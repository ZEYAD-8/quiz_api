from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .serializers import UserCustomSerializer, UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

# class RegisterUserView(APIView):

#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({
#                 'message': 'User registered successfully.',
#                 'user': UserCustomSerializer(user).data
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            period = refresh.lifetime.total_seconds() / 3600
            return Response({
                'message': 'User registered successfully.',
                'user': UserCustomSerializer(user).data,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'time remaining': period
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginUserView(APIView):

#     @csrf_exempt
#     def post(self, request):
#         print(request.data)
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user:
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'Login successful.',
#                 'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh)
#             })
#         return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            period = refresh.lifetime.total_seconds() / 3600
            access_token_period = refresh.access_token.lifetime.total_seconds() / 3600
            return Response({
                'message': 'Login successful.',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'time remaining': period,
                'access_token lifetime': access_token_period,
                'user': UserCustomSerializer(user).data
            })
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.exceptions import TokenError
class RefreshTokenView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        refresh_token = request.data.get('refresh')
        try:
            refresh = RefreshToken(refresh_token)
            return Response({'access': str(refresh.access_token)})
        except TokenError:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


# class LogoutUserView(APIView):

#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         logout(request)
#         return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        info = {
            'id': user.id,
            'email': user.email,
            'is_creator': user.is_creator,
            'is_admin': user.is_admin,
        }
        if user.is_creator:
            info['created_quizzes'] = [quiz.title for quiz in user.created_quizzes()]
        return Response(info, status=status.HTTP_200_OK)
