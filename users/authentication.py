from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication

User = get_user_model()


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# overriding TokenAuthentication class to use custom keyword
# and then let django continue with the rest of the process
class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        token = request.headers.get(self.keyword)
        if not token:
            return None

        return self.authenticate_credentials(token)
