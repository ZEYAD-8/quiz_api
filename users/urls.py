from django.urls import path
from .views import RegisterUserView, LoginUserView, UserProfileView, UserCreationsView, ChangePasswordView, ChangeRoleView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),

    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('change_role/', ChangeRoleView.as_view(), name='change_role'),

    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('creations/', UserCreationsView.as_view(), name='user_creations'),
]
