from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class CustomBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        usermodel = get_user_model()
        try:
            user = usermodel.objects.get(email=email)
        except usermodel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        usermodel = get_user_model()
        try:
            return usermodel.objects.get(pk=user_id)
        except usermodel.DoesNotExist:
            return None
