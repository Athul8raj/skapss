from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from tokens.token import check_pwd_rest_token,user_token
import datetime,pytz
from tokens.models import TM_USER_TOKEN
from org_hierarchy.user_crud_class import UserSerializer
from tm_users.models import TM_USER


@csrf_exempt
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
        try:
            check_user_already_login = TM_USER_TOKEN.objects.filter(email=email)
            if check_user_already_login:
                check_user_already_login.delete()       
        except ObjectDoesNotExist:
            check_user_already_login = None        
        if 'random1234' in password:
            return Response({'error': 'RESET_PASSWORD'},status=HTTP_200_OK)
        match_password = check_password(password,user.password)
        if match_password:
            token = user_token.make_token()
            new_user_token = TM_USER_TOKEN(email=email,
                                           timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
                                           token_id=token)
            new_user_token.save()
            try:
                get_user = TM_USER.objects.get(username=user.username)
                get_user_data = UserSerializer(get_user).data
                return Response({'token': token,'status':HTTP_200_OK,'payload':get_user_data},status=HTTP_200_OK,)
            except ObjectDoesNotExist:
                return Response({'token': token,'status':HTTP_200_OK,'payload':[]},status=HTTP_200_OK,)
        else:
            return Response({'error': 'AUTH_PASSWORD_NOT_VALID'},
                        status=HTTP_422_UNPROCESSABLE_ENTITY)
    except ObjectDoesNotExist:
        return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        
        
@csrf_exempt
@api_view(["POST"])
def update_pwd(request,token):
    password = request.data.get("password")
    _,user = check_pwd_rest_token(token)
    if password:
        update_pwd_user = User.objects.get(email=user.email)
        update_pwd_user.set_password(password)
        update_pwd_user.save()
        return Response({'success': 'PASSWORD_UPDATED','status':HTTP_200_OK,'error':None}
                        ,status=HTTP_200_OK)
    else:
        return Response({'error': 'CANNOT_UPDATE_PASSWORD'},status=HTTP_404_NOT_FOUND)
        

@csrf_exempt
@api_view(["POST"])
def logout(request):
    token =request.headers.get('Authorization')
    if token:
        request.session.flush()
        try:
            del_token = TM_USER_TOKEN.objects.filter(token_id=token)
            del_token.delete()
            return Response({'success':'LOGGING_OUT','status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'TOKEN_EXPIRED'},status=HTTP_401_UNAUTHORIZED)            
    else:
        return Response({'error': 'INVALID_REQUEST'},status=HTTP_400_BAD_REQUEST)       

