from .pwd_token_generator import PasswordResetTokenGenerator_Seconds_Expiration
from django.contrib.auth.models import User
from .models import PWD_RESET_TOKEN
from django.core.exceptions import ObjectDoesNotExist

pwd_reset_token = PasswordResetTokenGenerator_Seconds_Expiration()

def make_random_token(email):
    try:
        user = User.objects.get(email=email)
        make_pwd_token = pwd_reset_token.make_token(user)
        token_save = PWD_RESET_TOKEN(token_id=make_pwd_token,email=email)
        token_save.save()
        return make_pwd_token
    except ObjectDoesNotExist:
        return None 


def check_pwd_rest_token(token):
    try:
        token_id = PWD_RESET_TOKEN.objects.get(token_id=token)
        email = token_id.email
        user = User.objects.get(email=email)
        check_token_bool = pwd_reset_token.check_token(user,token)
        return check_token_bool
    except ObjectDoesNotExist:
        return None