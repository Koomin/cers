from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.base_user import BaseUserManager

from cers.cers_auth.models import CersUser


class LoginBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = CersUser.objects.get(**{'username__iexact': username})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user