from Duolingo.mysite.database.models import (UserProfile, RefreshToken, Follow, SuperFollow, FamilyFollow,
                                             MaxFollow, Language, Course, Lesson, Exercise, Option,
                                             UserProgress, XPHistory, Streak, Chat, ChatMember, Message,
                                             AddFriends, Country, Rating, LessonLevel, Achievement,
                                             UserAchievement, LessonCompletion)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]

class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.token]

class FollowAdmin(ModelView, model=Follow):
    column_list = [Follow.following_id, Follow.follower_id]

class SuperFollowAdmin(ModelView, model=SuperFollow):
    column_list = [SuperFollow.title]

class FamilyFollowAdmin(ModelView, model=FamilyFollow):
    column_list = [FamilyFollow.title]

class MaxFollowAdmin(ModelView, model=MaxFollow):
    column_list = [MaxFollow.title]

class LanguageAdmin(ModelView, model=Language):
    column_list = [Language.name]

class CourseAdmin(ModelView, model=Course):
    column_list = [Course.title]

class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.title]

class ExerciseAdmin(ModelView, model=Exercise):
    column_list = [Exercise.questions]

class OptionAdmin(ModelView, model=Option):
    column_list = [Option.exercise_id]

class UserProgressAdmin(ModelView, model=UserProgress):
    column_list = [UserProgress.completed]

class XPHistoryAdmin(ModelView, model=XPHistory):
    column_list = [XPHistory.reason]

class StreakAdmin(ModelView, model=Streak):
    column_list = [Streak.current_streak]

class ChatAdmin(ModelView, model=Chat):
    column_list = [Chat.type]

class ChatMemberAdmin(ModelView, model=ChatMember):
    column_list = [ChatMember.joined_at]

class MessageAdmin(ModelView, model=Message):
    column_list = [Message.content]

class AddFriendsAdmin(ModelView, model=AddFriends):
    column_list = [AddFriends.user_id]

class CountryAdmin(ModelView, model=Country):
    column_list = [Country.country_image, Country.country_name]

class RatingAdmin(ModelView, model=Rating):
    column_list = [Rating.user_id, Rating.streak_id]

class LessonLevelAdmin(ModelView, model=LessonLevel):
    column_list = [LessonLevel.level]

class LessonCompletionAdmin(ModelView, model=LessonCompletion):
    column_list = [LessonCompletion.date_completed]

class AchievementAdmin(ModelView, model=Achievement):
    column_list = [Achievement.title]

class UserAchievementAdmin(ModelView, model=UserAchievement):
    column_list = [UserAchievement.date_received]
