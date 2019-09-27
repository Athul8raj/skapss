import random as r
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import datetime,pytz
from .models import TM_PWD_TOKEN
from django.core.exceptions import ObjectDoesNotExist


EXPIRE_SECS = getattr(settings, 'PASSWORD_RESET_TIMEOUT_SECONDS', 1800)


class PasswordResetTokenGenerator_Seconds_Expiration:
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """

    def make_token(self):
        """
        Return a token that can be used once to do a token check
        for the given user.
        """
        return self.make_uuid()

    def make_uuid(self):
        random_string = ''
        random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        uuid_format = [8, 4, 4, 4, 12]
        for n in uuid_format:
            for i in range(0,n):
                random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
            if n != 12:
                random_string += '-'
        
        return random_string

    def check_token(self, token):
        try:
            token = TM_PWD_TOKEN.objects.get(token_id=token)
            if token.timestamp > timezone.now() - timedelta(seconds=EXPIRE_SECS):
                return True
            elif token.timestamp - timezone.now() > timedelta(hours=1):
                token.delete()
                return False
            else:
                return False
        except ObjectDoesNotExist:
            return False
       