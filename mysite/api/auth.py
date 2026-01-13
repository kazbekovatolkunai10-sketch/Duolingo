from fastapi import  APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import UserProfile
from Duolingo.mysite.database.schema import UserProfileInputSchema, UserProfileOutSchema, UserProfileLoginSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from
