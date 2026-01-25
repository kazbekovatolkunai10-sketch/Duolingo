from sqladmin import ModelView

from mysite.database.models import (
    UserProfile, RefreshToken, Follow, SuperFollow, FamilyFollow, MaxFollow,
    Language, Course, Lesson, Exercise, Option, UserProgres, XPHistory, Streak,
    AddFriends, Country, Rating, LessonLevel, Achievement, UserAchievement, LessonCompletion,
    # ✅ NEW CHAT MODELS
    ChatGroup, GroupPeople, ChatMessage, ChatReadState
)


class UserProfileAdmin(ModelView, model=UserProfile):
    name = "User"
    name_plural = "Users"
    column_list = ["id", "first_name", "last_name", "username", "email", "role", "is_active", "date_register"]
    column_searchable_list = ["first_name", "last_name", "username", "email"]
    column_sortable_list = ["id", "date_register", "username", "email", "is_active"]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    name = "Refresh Token"
    name_plural = "Refresh Tokens"
    column_list = ["id", "user_id", "token", "created_date"]
    column_searchable_list = ["token"]
    column_sortable_list = ["id", "created_date", "user_id"]


class FollowAdmin(ModelView, model=Follow):
    name = "Follow"
    name_plural = "Follows"
    column_list = ["id", "following_id", "follower_id", "following", "follower"]

    column_formatters = {
        "following": lambda m, a: m.following.username if m.following else None,
        "follower": lambda m, a: m.follower.username if m.follower else None,
    }


class SuperFollowAdmin(ModelView, model=SuperFollow):
    name = "Super Follow"
    name_plural = "Super Follows"
    column_list = ["id", "title", "description"]
    column_searchable_list = ["title"]
    column_sortable_list = ["id", "title"]


class FamilyFollowAdmin(ModelView, model=FamilyFollow):
    name = "Family Follow"
    name_plural = "Family Follows"
    column_list = ["id", "title", "description"]
    column_searchable_list = ["title"]
    column_sortable_list = ["id", "title"]


class MaxFollowAdmin(ModelView, model=MaxFollow):
    name = "Max Follow"
    name_plural = "Max Follows"
    column_list = ["id", "title", "description"]
    column_searchable_list = ["title"]
    column_sortable_list = ["id", "title"]


class LanguageAdmin(ModelView, model=Language):
    name = "Language"
    name_plural = "Languages"
    column_list = ["id", "code", "name", "is_active"]
    column_searchable_list = ["code", "name"]
    column_sortable_list = ["id", "code", "name", "is_active"]


class CourseAdmin(ModelView, model=Course):
    name = "Course"
    name_plural = "Courses"
    column_list = ["id", "language_id", "title", "level", "order"]
    column_searchable_list = ["title"]
    column_sortable_list = ["id", "order", "language_id"]


class LessonAdmin(ModelView, model=Lesson):
    name = "Lesson"
    name_plural = "Lessons"
    column_list = ["id", "course_id", "title", "order", "is_locked", "xp_reward"]
    column_searchable_list = ["title"]
    column_sortable_list = ["id", "course_id", "order", "is_locked", "xp_reward"]


class ExerciseAdmin(ModelView, model=Exercise):
    name = "Exercise"
    name_plural = "Exercises"
    column_list = ["id", "lesson_id", "type", "questions", "correct_answer"]
    column_searchable_list = ["questions", "correct_answer"]
    column_sortable_list = ["id", "lesson_id", "type"]


class OptionAdmin(ModelView, model=Option):
    name = "Option"
    name_plural = "Options"
    column_list = ["id", "exercise_id", "exercise"]
    column_sortable_list = ["id", "exercise_id"]

    column_formatters = {
        "exercise": lambda m, a: (
            (m.exercise.questions[:80] + "…")
            if (m.exercise and m.exercise.questions and len(m.exercise.questions) > 80)
            else (m.exercise.questions if m.exercise else None)
        )
    }


class UserProgresAdmin(ModelView, model=UserProgres):
    name = "User Progress"
    name_plural = "User Progress"
    column_list = ["id", "user_id", "lesson_id", "completed", "score", "xp_earned", "completed_date"]
    column_sortable_list = ["id", "user_id", "lesson_id", "completed", "score", "completed_date"]


class XPHistoryAdmin(ModelView, model=XPHistory):
    name = "XP History"
    name_plural = "XP History"
    column_list = ["id", "user_id", "xp", "reason", "created_date"]
    column_searchable_list = ["reason"]
    column_sortable_list = ["id", "user_id", "xp", "created_date"]


class StreakAdmin(ModelView, model=Streak):
    name = "Streak"
    name_plural = "Streaks"
    column_list = ["id", "user_id", "current_steak", "last_activity"]
    column_sortable_list = ["id", "user_id", "current_steak", "last_activity"]


class AddFriendsAdmin(ModelView, model=AddFriends):
    name = "Add Friend"
    name_plural = "Add Friends"
    column_list = ["id", "user_id", "add_user"]

    column_formatters = {
        "add_user": lambda m, a: m.add_user.username if m.add_user else None
    }


class CountryAdmin(ModelView, model=Country):
    name = "Country"
    name_plural = "Countries"
    column_list = ["id", "user_id", "user_country"]

    column_formatters = {
        "user_country": lambda m, a: m.user_country.username if m.user_country else None
    }


class RatingAdmin(ModelView, model=Rating):
    name = "Rating"
    name_plural = "Ratings"
    column_list = ["id", "user_id", "streak_id", "user_rating", "streak_rating"]

    column_formatters = {
        "user_rating": lambda m, a: m.user_rating.username if m.user_rating else None,
        "streak_rating": lambda m, a: m.streak_rating.current_steak if m.streak_rating else None,
    }


class LessonLevelAdmin(ModelView, model=LessonLevel):
    name = "Lesson Level"
    name_plural = "Lesson Levels"
    column_list = ["id", "user_id", "lesson_id", "level", "experience", "max_level"]
    column_sortable_list = ["id", "user_id", "lesson_id", "level", "experience"]


class LessonCompletionAdmin(ModelView, model=LessonCompletion):
    name = "Lesson Completion"
    name_plural = "Lesson Completions"
    column_list = ["id", "user_id", "lesson_id", "date_completed"]
    column_sortable_list = ["id", "user_id", "lesson_id", "date_completed"]


class AchievementAdmin(ModelView, model=Achievement):
    name = "Achievement"
    name_plural = "Achievements"
    column_list = ["id", "title", "code"]
    column_searchable_list = ["title", "code"]
    column_sortable_list = ["id", "title", "code"]


class UserAchievementAdmin(ModelView, model=UserAchievement):
    name = "User Achievement"
    name_plural = "User Achievements"
    column_list = ["id", "user_id", "achievement_id", "date_received"]
    column_sortable_list = ["id", "user_id", "achievement_id", "date_received"]


# =========================
# ✅ CHAT ADMIN (НОВЫЕ МОДЕЛИ)
# =========================
class ChatGroupAdmin(ModelView, model=ChatGroup):
    name = "Chat Group"
    name_plural = "Chat Groups"
    column_list = ["id", "owner_id", "title", "is_private", "create_date"]
    column_searchable_list = ["title"]
    column_sortable_list = ["id", "create_date", "owner_id", "is_private"]


class GroupPeopleAdmin(ModelView, model=GroupPeople):
    name = "Group Member"
    name_plural = "Group Members"
    column_list = ["id", "group_id", "user_id", "joined_date"]
    column_sortable_list = ["id", "group_id", "user_id", "joined_date"]


class ChatMessageAdmin(ModelView, model=ChatMessage):
    name = "Chat Message"
    name_plural = "Chat Messages"
    column_list = ["id", "group_id", "user_id", "text", "is_deleted", "created_date", "edited_at"]
    column_searchable_list = ["text"]
    column_sortable_list = ["id", "group_id", "user_id", "created_date", "is_deleted"]


class ChatReadStateAdmin(ModelView, model=ChatReadState):
    name = "Read State"
    name_plural = "Read States"
    column_list = ["id", "group_id", "user_id", "last_read_message_id", "updated_at"]
    column_sortable_list = ["id", "group_id", "user_id", "updated_at"]
