from django.urls import path
from .views import RegisterUserView, LoginUserView, UserProfileView, RefreshTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
)
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    # path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    
    
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
