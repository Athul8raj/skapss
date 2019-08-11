from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN ,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from tokens.token import check_pwd_rest_token,user_token
import datetime,pytz
from tokens.models import TM_USER_TOKEN
from tokens.token import check_token_validity
from .models import TM_USER,TM_USER_CONTACT,TM_USER_GROUP


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
        if 'random1234' in password:
            return Response({'error': 'RESET_PASSWORD'},status=HTTP_200_OK)
        match_password = check_password(password,user.password)
        if match_password:
            token = user_token.make_token(user)
            new_user_token = TM_USER_TOKEN(email=email,
                                           timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
                                           token_id=token)
            new_user_token.save()
            return Response({'token': token,'status':HTTP_200_OK,'error':None},
                    status=HTTP_200_OK)
        else:
            return Response({'error': 'AUTH_PASSWORD_NOT_VALID'},
                        status=HTTP_403_FORBIDDEN)
    except ObjectDoesNotExist:
        return Response({'error': 'MEMBER_NOT_FOUND',},
                        status=HTTP_404_NOT_FOUND)
        
        
@csrf_exempt
@api_view(["POST"])
def update_pwd(request,token):
    password = request.data.get("password")
    _,user = check_pwd_rest_token(token)
    if password:
        update_pwd_user = User.objects.get(email=user.email)
        update_pwd_user.set_password(password)
        update_pwd_user.save()
        return Response({'success': 'Password successfully updated','status':HTTP_200_OK,'error':None}
                        ,status=HTTP_200_OK)
    else:
        return Response({'error': 'Cannot update password'},
                        status=HTTP_404_NOT_FOUND)
        

###########----------for user-group------------##################
        
@csrf_exempt
@api_view(["GET"])
def get_all_user_data(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            all_data_array = []
            try:
                get_all_user_grp_data = TM_USER_GROUP.objects.get(is_deleted=False)
                get_all_users = TM_USER.objects.get(is_deleted=False)
                all_data_array.append(get_all_user_grp_data)
                all_data_array.append(get_all_users)
                if not new_token:
                    return Response({'success':f'ALL_DATA_FOUND','data':all_data_array},status=HTTP_200_OK)
                else:
                    return Response({'success':f'ALL_DATA_FOUND','token':new_token,'data':all_data_array},status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Token Expired'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Invalid Request'},
                        status=HTTP_400_BAD_REQUEST)
        
@csrf_exempt
@api_view(["POST"])
def add_user_group(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            group_name = request.data.get('name')
            group_desc = request.data.get('desc')
            group_org_id = request.data.get('org_id')
            group_dept_id = request.data.get('dept_id')
            group_div_id = request.data.get('div_id')
            group_post_id = request.data.get('post_id')
            group_id = f'{group_name[:2]}2019'
            user_group_add = TM_USER_GROUP(group_id=group_id,group_name=group_name,group_desc=group_desc,
                                           group_org_id=group_org_id,group_dept_id=group_dept_id,
                                           group_div_id=group_div_id,group_post_id=group_post_id,created_by=old_token.email)
            user_group_add.save()
            if not new_token:
                return Response({'success':'USER_GROUP_ADDED'},status=HTTP_200_OK)
            else:
                return Response({'success':'USER_GROUP_ADDED','token':new_token},
                                    status=HTTP_200_OK)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["GET"])
def view_user_group(request,grp_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            try:
                get_user_group = TM_USER_GROUP(group_id=grp_id,is_deleted=False)
                if not new_token:
                    return Response({'success':'USER_GROUP_ADDED','data':get_user_group},status=HTTP_200_OK)
                else:
                    return Response({'success':'USER_GROUP_ADDED','data':get_user_group,'token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        


@csrf_exempt
@api_view(["DELETE"])
def del_user_group(request,grp_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_user_group = TM_USER_GROUP(group_id=grp_id,is_deleted=False)
                get_user_group.soft_delete(old_token.email)
                if not new_token:
                    return Response({'success':'USER_GROUP_DELETED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'USER_GROUP_DELETED','token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["PUT"])
def update_user_group(request,grp_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            group_name = request.data.get('name')
            group_desc = request.data.get('desc')
            group_org_id = request.data.get('org_id')
            group_dept_id = request.data.get('dept_id')
            group_div_id = request.data.get('div_id')
            group_post_id = request.data.get('post_id')
            group_id = f'{group_name[:2]}2019'
            try:
                get_user_group = TM_USER_GROUP(group_id=grp_id,is_deleted=False)
                get_user_group.update(group_id=group_id,group_name=group_name,group_desc=group_desc,
                                           group_org_id=group_org_id,group_dept_id=group_dept_id,
                                           group_div_id=group_div_id,group_post_id=group_post_id,modified_by=old_token.email)
                if not new_token:
                    return Response({'success':'USER_GROUP_UPDATED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'USER_GROUP_UPDATED','token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

#############-----------for user----------##########

@csrf_exempt
@api_view(["POST"])
def add_user(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            username = request.data.get('name')
            user_id = f'{username[:2]}2019'
            user_addr1 = request.data.get('address')
            user_dept_id = request.data.get('dept')
            user_div_id = request.data.get('div')
            user_group_id = request.data.get('user_group')
            user_org_id = request.data.get('org')
            user_post_id = request.data.get('post')
            user_resp_id = request.data.get('resp')
            user_mobile_num = request.data.get('mobile')
            user_email_id = request.data.get('email')
            user_cont_id = f'{username[:2]}ADD2019'
            user_cont_addr2 = request.data.get('address2')
            user_cont_addr3 = request.data.get('address3')
            user_cont_city = request.data.get('city')
            user_cont_state = request.data.get('state')
            user_cont_country_code = request.data.get('country')
            user_cont_zip_code = request.data.get('zipcode')
            user_mobile_num2 = request.data.get('mobile2')
            user_email_id2 = request.data.get('email2')
            user_add = TM_USER(user_id=user_id,username=username,user_addr1=user_addr1,user_dept_id=user_dept_id,
                               user_div_id=user_div_id,user_group_id=user_group_id,user_org_id=user_org_id,
                               user_post_id=user_post_id,user_resp_id=user_resp_id,user_mobile_num=user_mobile_num,
                               user_email_id=user_email_id,created_by=old_token.email)
            user_contact_add = TM_USER_CONTACT(user_cont_id=user_cont_id,user_cont_addr2=user_cont_addr2,user_cont_addr3=user_cont_addr3,
                                               user_cont_city=user_cont_city,user_cont_state=user_cont_state,user_cont_country_code=user_cont_country_code,
                                               user_cont_zip_code=user_cont_zip_code,user_mobile_num2=user_mobile_num2,user_email_id2=user_email_id2,
                                               created_by=old_token.email)
            user_add.save()
            user_contact_add.save()
            if not new_token:
                return Response({'success':'USER_ADDED'},status=HTTP_200_OK)
            else:
                return Response({'success':'USER_ADDED','token':new_token},
                                    status=HTTP_200_OK)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["GET"])
def view_user(request,user_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            all_data_user = []
            try:
                get_user = TM_USER(user_id=user_id,is_deleted=False)
                get_user_contact = TM_USER_CONTACT(user_id=user_id,is_deleted=False)
                all_data_user.append(get_user)
                all_data_user.append(get_user_contact)
                if not new_token:
                    return Response({'success':'USER_GROUP_ADDED','data':all_data_user},status=HTTP_200_OK)
                else:
                    return Response({'success':'USER_GROUP_ADDED','data':all_data_user,'token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        


@csrf_exempt
@api_view(["DELETE"])
def del_user(request,user_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_user = TM_USER(user_id=user_id,is_deleted=False)
                get_user_contact = TM_USER_CONTACT(user_id=user_id,is_deleted=False)
                get_user.soft_delete(old_token.email)
                get_user_contact.soft_delete(old_token.email)
                if not new_token:
                    return Response({'success':'USER_DELETED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'USER_DELETED','token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["PUT"])
def update_user(request,user_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            username = request.data.get('name')
            user_id = f'{username[:2]}2019'
            user_addr1 = request.data.get('address')
            user_dept_id = request.data.get('dept')
            user_div_id = request.data.get('div')
            user_group_id = request.data.get('user_group')
            user_org_id = request.data.get('org')
            user_post_id = request.data.get('post')
            user_resp_id = request.data.get('resp')
            user_mobile_num = request.data.get('mobile')
            user_email_id = request.data.get('email')
            user_cont_id = f'{username[:2]}ADD2019'
            user_cont_addr2 = request.data.get('address2')
            user_cont_addr3 = request.data.get('address3')
            user_cont_city = request.data.get('city')
            user_cont_state = request.data.get('state')
            user_cont_country_code = request.data.get('country')
            user_cont_zip_code = request.data.get('zipcode')
            user_mobile_num2 = request.data.get('mobile2')
            user_email_id2 = request.data.get('email2')
            try:
                get_user = TM_USER(user_id=user_id,is_deleted=False)
                get_user_contact = TM_USER_CONTACT(user_id=user_id,is_deleted=False)
                get_user.update(user_id=user_id,username=username,user_addr1=user_addr1,user_dept_id=user_dept_id,
                               user_div_id=user_div_id,user_group_id=user_group_id,user_org_id=user_org_id,
                               user_post_id=user_post_id,user_resp_id=user_resp_id,user_mobile_num=user_mobile_num,
                               user_email_id=user_email_id,modified_by=old_token.email)
                get_user_contact.update(user_cont_id=user_cont_id,user_cont_addr2=user_cont_addr2,user_cont_addr3=user_cont_addr3,
                                               user_cont_city=user_cont_city,user_cont_state=user_cont_state,user_cont_country_code=user_cont_country_code,
                                               user_cont_zip_code=user_cont_zip_code,user_mobile_num2=user_mobile_num2,
                                               user_email_id2=user_email_id2,modified_by=old_token.email)
                if not new_token:
                    return Response({'success':'USER_DETAILS_UPDATED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'USER_DETAILS_UPDATED','token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

    
       
        
        
    