from typing import Dict, Set, List, Optional, Any
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models_chat import (
    UserProfile,
    GroupPeople,
    ChatMessage,
    ChatReadState,
)
from mysite.config import SECRET_KEY, ALGORITHM

ws_router = APIRouter(tags=["WS Messages"])


# -------- JWT for WS --------
def _extract_token(websocket: WebSocket, token_q: Optional[str]) -> Optional[str]:
    if token_q:
        return token_q
    auth = websocket.headers.get("authorization")
    if not auth:
        return None
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def get_user_from_token(db: Session, token: str) -> UserProfile:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise JWTError("no sub")
    except JWTError:
        raise ValueError("Invalid token")

    user = db.query(UserProfile).filter(UserProfile.id == int(user_id)).first()
    if not user:
        raise ValueError("User not found")
    return user


async def _reject(websocket: WebSocket, detail: str, code: int = 1008) -> None:
    await websocket.accept()
    await websocket.send_json({"event": "error", "detail": detail})
    await websocket.close(code=code)


# -------- Connection manager --------
class ConnectionManager:
    def __init__(self) -> None:
        self._connections: Dict[int, Set[WebSocket]] = {}
        self._active_chat: Dict[WebSocket, Optional[int]] = {}  # ws -> group_id (opened chat)

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        self._connections.setdefault(user_id, set()).add(websocket)
        self._active_chat[websocket] = None

    def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        if user_id in self._connections:
            self._connections[user_id].discard(websocket)
            if not self._connections[user_id]:
                self._connections.pop(user_id, None)
        self._active_chat.pop(websocket, None)

    def set_active_chat(self, websocket: WebSocket, group_id: Optional[int]) -> None:
        self._active_chat[websocket] = group_id

    def is_chat_active_for_user(self, user_id: int, group_id: int) -> bool:
        for ws in self._connections.get(user_id, []):
            if self._active_chat.get(ws) == group_id:
                return True
        return False

    async def send_to_user(self, user_id: int, payload: dict) -> None:
        conns = list(self._connections.get(user_id, []))
        dead: List[WebSocket] = []
        for ws in conns:
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(user_id, ws)

    async def broadcast(self, user_ids: List[int], payload: dict) -> None:
        for uid in set(user_ids):
            await self.send_to_user(uid, payload)


manager = ConnectionManager()


# -------- DB helpers --------
def is_member(db: Session, group_id: int, user_id: int) -> bool:
    return db.query(GroupPeople).filter(
        GroupPeople.group_id == group_id,
        GroupPeople.user_id == user_id
    ).first() is not None


def group_member_ids(db: Session, group_id: int) -> List[int]:
    rows = db.query(GroupPeople.user_id).filter(GroupPeople.group_id == group_id).all()
    return [r[0] for r in rows]


def msg_to_dict(m: ChatMessage) -> dict:
    return {
        "id": m.id,
        "group_id": m.group_id,
        "user_id": m.user_id,
        "text": "" if getattr(m, "is_deleted", False) else m.text,
        "is_deleted": getattr(m, "is_deleted", False),
        "edited_at": m.edited_at.isoformat() if getattr(m, "edited_at", None) else None,
        "created_date": m.created_date.isoformat() if m.created_date else None,
    }


def upsert_read_state(db: Session, group_id: int, user_id: int, message_id: int) -> int:
    """
    ✅ Обновляет ChatReadState (не откатываем назад) и возвращает last_read_message_id
    """
    state = db.query(ChatReadState).filter(
        ChatReadState.group_id == group_id,
        ChatReadState.user_id == user_id
    ).first()

    if not state:
        state = ChatReadState(
            group_id=group_id,
            user_id=user_id,
            last_read_message_id=message_id,
            updated_at=datetime.utcnow()
        )
        db.add(state)
        return message_id

    if state.last_read_message_id is None or message_id > state.last_read_message_id:
        state.last_read_message_id = message_id
        state.updated_at = datetime.utcnow()

    return state.last_read_message_id or message_id


# -------- WebSocket --------
@ws_router.websocket("/ws/messages")
async def ws_messages(websocket: WebSocket, token: Optional[str] = Query(default=None)):
    db = SessionLocal()
    user: Optional[UserProfile] = None

    try:
        tok = _extract_token(websocket, token)
        if not tok:
            await _reject(websocket, "Missing token")
            return

        try:
            user = get_user_from_token(db, tok)
        except ValueError as e:
            await _reject(websocket, str(e))
            return

        await websocket.accept()
        await manager.connect(user.id, websocket)

        await websocket.send_json({"event": "connected", "user_id": user.id})

        while True:
            data: Dict[str, Any] = await websocket.receive_json()
            action = data.get("action")

            # ✅ set active chat (chat opened)
            if action == "set_active_chat":
                group_id = data.get("group_id")
                if not isinstance(group_id, int):
                    await websocket.send_json({"event": "error", "detail": "group_id(int) required"})
                    continue

                if not is_member(db, group_id, user.id):
                    await websocket.send_json({"event": "error", "detail": "not a member"})
                    continue

                manager.set_active_chat(websocket, group_id)
                await websocket.send_json({"event": "active_chat_set", "group_id": group_id})
                continue

            # ✅ clear active chat (chat closed)
            if action == "clear_active_chat":
                manager.set_active_chat(websocket, None)
                await websocket.send_json({"event": "active_chat_cleared"})
                continue

            # ✅ send message
            group_id = data.get("group_id")
            text = (data.get("text") or "").strip()

            if not isinstance(group_id, int) or not text:
                await websocket.send_json({"event": "error", "detail": "group_id(int) and text required"})
                continue

            if not is_member(db, group_id, user.id):
                await websocket.send_json({"event": "error", "detail": "not a member"})
                continue

            m = ChatMessage(group_id=group_id, user_id=user.id, text=text)
            db.add(m)
            db.commit()
            db.refresh(m)

            members = group_member_ids(db, group_id)

            # ✅ AUTO-READ + READ RECEIPT (receipt -> only to sender)
            receipts: List[dict] = []
            for uid in members:
                if uid == user.id:
                    continue
                if manager.is_chat_active_for_user(uid, group_id):
                    last_read = upsert_read_state(db, group_id=group_id, user_id=uid, message_id=m.id)
                    receipts.append({
                        "event": "read_receipt",
                        "group_id": group_id,
                        "reader_id": uid,
                        "last_read_message_id": last_read
                    })

            db.commit()

            # 1) всем участникам сообщение
            await manager.broadcast(members, {"event": "message", "message": msg_to_dict(m)})

            # 2) receipt ТОЛЬКО автору (как Telegram)
            for rr in receipts:
                await manager.send_to_user(user.id, rr)

    except WebSocketDisconnect:
        pass
    finally:
        if user is not None:
            manager.disconnect(user.id, websocket)
        db.close()
