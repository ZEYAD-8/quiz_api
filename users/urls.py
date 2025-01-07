from django.urls import path
from .views import RegisterUserView, LoginUserView, UserProfileView, UserCreatedQuizzesView, UserCreatedQuestionsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('created_quizzes/', UserCreatedQuizzesView.as_view(), name='user_created_quizzes'),
    path('created_questions/', UserCreatedQuestionsView.as_view(), name='user_created_questions'),
]
