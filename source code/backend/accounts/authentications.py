from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .models import User

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Authorization header is missing or invalid")

        token = auth_header.split(' ')[1]
        try:
            # Giải mã token và lấy user_id
            decoded_token = AccessToken(token)
            user_id = decoded_token.payload.get('user_id')

            if not user_id:
                raise AuthenticationFailed("Token is missing user information")

            # Lấy user từ DB
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed("User not found")

            return (user, None)
        except Exception as e:
            raise AuthenticationFailed(f"Invalid or expired token: {str(e)}")