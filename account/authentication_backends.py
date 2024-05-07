from django.contrib.auth.backends import BaseBackend
from django.utils import timezone
from django.conf import settings

from account.models import User  # Assuming your user model is in account.models

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                user.failed_login_attempts = 0  # Reset failed login attempts upon successful login
                user.save()
                return user
            else:
                user.failed_login_attempts += 1  # Increment failed login attempts
                if user.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
                    user.is_blocked = True
                    user.blocked_until = timezone.now() + settings.ACCOUNT_LOCKOUT_DURATION
                    user.save()
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
