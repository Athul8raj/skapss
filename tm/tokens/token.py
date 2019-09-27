from .pwd_token_generator import PasswordResetTokenGenerator_Seconds_Expiration
from .user_token_generator import User_token_generator
from django.contrib.auth.models import User
from .models import TM_PWD_TOKEN,TM_USER_TOKEN
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
import datetime,pytz

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 1)

pwd_reset_token = PasswordResetTokenGenerator_Seconds_Expiration()
user_token = User_token_generator()

########-----for password----------#########


def make_random_pwd_token(email):
    try:
        user = User.objects.get(email=email)
        make_pwd_token = pwd_reset_token.make_token()
        token_save = TM_PWD_TOKEN(token_id=make_pwd_token,email=email)
        token_save.save()
        return make_pwd_token,user
    except ObjectDoesNotExist:
        return None,None


def check_pwd_rest_token(token):
    try:
        token_id = TM_PWD_TOKEN.objects.get(token_id=token) 
        email = token_id.email
        user = User.objects.get(email=email)
        check_token_bool = pwd_reset_token.check_token(token)
        return check_token_bool,user
    except ObjectDoesNotExist:
        return None,None
    
#########----------for user------------##############
    
def check_token_validity(token):
    try:
        token = TM_USER_TOKEN.objects.filter(token_id=token).first()
        if token.timestamp > timezone.now() - timedelta(hours=EXPIRE_HOURS):
            new_token = TM_USER_TOKEN(token_id=token.token_id,timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.utc),email=token.email)
            new_token.save()
            token = TM_USER_TOKEN.objects.filter(token_id=token)
            token.delete()
            return True,None,new_token
        elif token.timestamp - timezone.now() > timedelta(hours=1):
            new_token = user_token.make_token()
            new_user_token = TM_USER_TOKEN(email=token.email,token_id=new_token,timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.utc))
            new_user_token.save()
            token = TM_USER_TOKEN.objects.filter(token_id=token)
            token.delete()
            return False,new_token,None
        else:
            return False,None,token
    except ObjectDoesNotExist:
        return None,None,None