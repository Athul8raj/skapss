from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
#        if 'random1234' in password:
#            return Response({'status_code': 'RESET_PASSWORD'})
        match_password = check_password(password,user.password)
        if match_password:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,'status':HTTP_200_OK,'error':None},
                    status=HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password. Please retype password or click Forgot Password?'},
                        status=HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist:
        return Response({'error': 'Invalid email',},
                        status=HTTP_404_NOT_FOUND)
    