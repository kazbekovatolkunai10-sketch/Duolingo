from .views import (UserProfileAdmin, FollowAdmin, SuperFollowAdmin,
                    FamilyFollowAdmin, MaxFollowAdmin, LanguageAdmin,
                    CourseAdmin, LessonAdmin, ExerciseAdmin,
                    OptionAdmin, UserProgressAdmin, XPHistoryAdmin,
                    StreakAdmin, ChatAdmin, ChatMemberAdmin,
                    MessageAdmin, AddFriendsAdmin, CountryAdmin,
                    RatingAdmin, LessonLevelAdmin, AchievementAdmin)
from fastapi import FastAPI
from sqladmin import Admin
from Duolingo.mysite.database.db import engine


def setup_admin(mysite_app: FastAPI):
    admin = Admin(mysite_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(FollowAdmin)
    admin.add_view(SuperFollowAdmin)
    admin.add_view(FamilyFollowAdmin)
    admin.add_view(MaxFollowAdmin)
    admin.add_view(LanguageAdmin)
    admin.add_view(CourseAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(ExerciseAdmin)
    admin.add_view(OptionAdmin)
    admin.add_view(UserProgressAdmin)
    admin.add_view(XPHistoryAdmin)
    admin.add_view(StreakAdmin)
    admin.add_view(ChatAdmin)
    admin.add_view(ChatMemberAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(AddFriendsAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(RatingAdmin)
    admin.add_view(LessonLevelAdmin)
    admin.add_view(AchievementAdmin)
