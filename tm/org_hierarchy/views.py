from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED   
)
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tokens.token import check_token_validity
from tm_users.models import (TM_ORG,TM_ORG_CONTACT,TM_DEPT,TM_DIV,TM_POST,
                             TM_ACCESS_VIEWS,TM_RESPONSIBILITY)


#########------------for organization------------#########

@csrf_exempt
@api_view(["GET"])
def get_all_hier_data(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            all_data_array = []
            try:
                get_all_org_data = TM_ORG.objects.get(is_deleted=False)
                get_all_dept_data = TM_DEPT.objects.get(is_deleted=False)
                get_all_div_data = TM_DIV.objects.get(is_deleted=False)
                get_all_post_data = TM_POST.objects.get(is_deleted=False)
                all_data_array.append(get_all_org_data)
                all_data_array.append(get_all_dept_data)
                all_data_array.append(get_all_div_data)
                all_data_array.append(get_all_post_data)
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
@api_view(["GET"])
def get_all_resp_view_data(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            all_data_array = []
            try:
                get_all_resp_data = TM_RESPONSIBILITY.objects.get(is_deleted=False)
                get_all_view_data = TM_ACCESS_VIEWS.objects.get(is_deleted=False)
                all_data_array.append(get_all_resp_data)
                all_data_array.append(get_all_view_data)
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
def add_org(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            org_name = request.data.get('name')
            org_address = request.data.get('address')
            org_ext = request.data.get('external')
            org_id = f'{org_name[:3]}2019'
            org_cont_id = f'{org_name[:3]}ADD2019'
            org_cont_addr2 = request.data.get('address2')
            org_cont_addr3 = request.data.get('address3')
            org_cont_city = request.data.get('city')
            org_cont_state = request.data.get('state')
            org_cont_country_code = request.data.get('country')
            org_cont_zip_code = request.data.get('zipcode')
            org_cont_phone = request.data.get('phone') 
            org_add = TM_ORG(org_id=org_id,org_name=org_name,org_address=org_address,org_ext=org_ext,created_by=old_token.email)
            org_contact_add = TM_ORG_CONTACT(org_id=org_id,org_cont_id=org_cont_id,org_cont_addr2=org_cont_addr2,
                                             org_cont_addr3=org_cont_addr3,org_cont_city=org_cont_city,
                                             org_cont_state=org_cont_state,org_cont_country_code=org_cont_country_code,
                                             org_cont_zip_code=org_cont_zip_code,org_cont_phone=org_cont_phone,created_by=old_token.email)
            org_add.save()
            org_contact_add.save()
            if not new_token:
                return Response({'success':f'{org_name.upper()}_ADDED'},status=HTTP_200_OK)
            else:
                return Response({'success':f'{org_name.upper()}_ADDED','token':new_token},status=HTTP_200_OK)
        else:
            return Response({'error': 'Token Expired'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Invalid Request'},
                        status=HTTP_400_BAD_REQUEST)          
    

@csrf_exempt
@api_view(["GET"])
def view_org(request,org_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            all_data_array = []
            try:
                get_org = TM_ORG.objects.get(org_id=org_id,is_deleted=False)
                get_org_contact = TM_ORG_CONTACT.objects.get(org_id=org_id,is_deleted=False)
                all_data_array.append(get_org)
                all_data_array.append(get_org_contact)
                if not new_token:
                    return Response({'success':'ORG_FOUND','data':all_data_array},status=HTTP_200_OK)
                else:
                    return Response({'success':'ORG_FOUND','data':all_data_array,'token':new_token},status=HTTP_200_OK)
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
def del_org(request,org_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_org = TM_ORG.objects.get(org_id=org_id,is_deleted=False)
                get_org_contact = TM_ORG_CONTACT.objects.get(org_id=org_id,is_deleted=False)
                if not new_token:
                    get_org.soft_delete(old_token.email)
                    get_org_contact.soft_delete(old_token.email)
                    return Response({'success':'ORG_DELETED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'ORG_DELETED','token':new_token},status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["PUT"])
def update_org(request,org_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_org = TM_ORG.objects.get(org_id=org_id,is_deleted=False)
                get_org_contact = TM_ORG_CONTACT.objects.get(org_id=org_id,is_deleted=False)
                org_name = request.data.get('name')
                org_address = request.data.get('address')
                org_ext = request.data.get('external')
                org_id = f'{org_name[:4]}2019'
                org_cont_id = f'{org_name[:3]}ADD2019'
                org_cont_addr2 = request.data.get('address2')
                org_cont_addr3 = request.data.get('address3')
                org_cont_city = request.data.get('city')
                org_cont_state = request.data.get('state')
                org_cont_country_code = request.data.get('country')
                org_cont_zip_code = request.data.get('zipcode')
                org_cont_phone = request.data.get('phone') 
                if not new_token:
                    get_org.update(org_id=org_id,org_name=org_name,org_address=org_address,org_ext=org_ext,modified_by=old_token.email)
                    get_org_contact.update(org_id=org_id,org_cont_id=org_cont_id,org_cont_addr2=org_cont_addr2,
                                             org_cont_addr3=org_cont_addr3,org_cont_city=org_cont_city,
                                             org_cont_state=org_cont_state,org_cont_country_code=org_cont_country_code,
                                             org_cont_zip_code=org_cont_zip_code,org_cont_phone=org_cont_phone,modified_by=old_token.email)
                    return Response({'success':'ORG_DETAILS_UPDATED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'ORG_DETAILS_UPDATED','token':new_token},status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        
###########-------for departments----------##########      

@csrf_exempt
@api_view(["POST"])
def add_dept(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
                dept_name = request.data.get('name')
                dept_desc = request.data.get('desc')
                dept_org_id = request.data.get('org')
                dept_id = f'{dept_name[:2]}2019'
                dept_add = TM_DEPT(dept_name=dept_name,dept_id=dept_id,dept_org_id=dept_org_id,dept_desc=dept_desc,created_by=old_token.email)
                dept_add.save()
                if not new_token:
                    return Response({'success':'DEPT_ADDED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'DEPT_ADDED','token':new_token},status=HTTP_200_OK)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["GET"])
def view_dept(request,dept_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            try:
                get_dept = TM_DEPT.objects.get(dept_id=dept_id,is_deleted=False)
                if not new_token:
                    return Response({'success':'DEPT_FOUND','dept_data':get_dept},status=HTTP_200_OK)
                else:
                    return Response({'success':'DEPT_FOUND','dept_data':get_dept,'token':new_token},status=HTTP_200_OK)
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
def del_dept(request,dept_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_dept = TM_DEPT.objects.get(dept_id=dept_id,is_deleted=False)
                if not new_token:
                    get_dept.soft_delete(old_token.email)
                    return Response({'success':'DEPT_DELETED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'DEPT_DELETED','token':new_token},status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["PUT"])
def update_dept(request,dept_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            dept_name = request.data.get('name')
            dept_desc = request.data.get('desc')
            dept_org_id = request.data.get('org')
            dept_id = f'{dept_name[:2]}2019'
            try:
                get_dept = TM_DEPT.objects.get(dept_id=dept_id,is_deleted=False)
                get_dept.update(dept_name=dept_name,dept_id=dept_id,
                                dept_org_id=dept_org_id,dept_desc=dept_desc,modified_by=old_token.email)
                if not new_token:
                    return Response({'success':'DEPT_DETAILS_UPDATED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'DEPT_DETAILS_UPDATED','token':new_token},status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        
        
        
##########---------for Divisions--------##############        

@csrf_exempt
@api_view(["POST"])
def add_div(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            div_name = request.data.get('name')
            div_desc = request.data.get('desc')
            div_org_id = request.data.get('org')
            div_dept_id = request.data.get('dept')
            div_id = f'{div_name[:2]}2019'
            div_add = TM_DIV(div_id=div_id,div_name=div_name,div_dept_id=div_dept_id,div_org_id=div_org_id,div_desc=div_desc,created_by=old_token.email)
            div_add.save()
            if not new_token:
                return Response({'success':'DIVISION_ADDED'},status=HTTP_200_OK)
            else:
                return Response({'success':'DIVISION_ADDED','token':new_token},status=HTTP_200_OK)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        


@csrf_exempt
@api_view(["GET"])
def view_div(request,div_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            try:
                get_div = TM_DEPT.objects.get(div_id=div_id,is_deleted=False)
                if not new_token:
                    return Response({'success':'DIVISION_FOUND','div_data':get_div},status=HTTP_200_OK)
                else:
                    return Response({'success':'DIVISION_FOUND','div_data':get_div,'token':new_token},status=HTTP_200_OK)
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
def del_div(request,div_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_div = TM_DEPT.objects.get(div_id=div_id,is_deleted=False)
                if not new_token:
                    get_div.soft_delete(old_token.email)
                    return Response({'success':'DIVISION_DELETED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'DIVISION_DELETED','token':new_token},status=HTTP_200_OK)
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
def update_div(request,div_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            div_name = request.data.get('name')
            div_desc = request.data.get('desc')
            div_org_id = request.data.get('org')
            div_dept_id = request.data.get('dept')
            div_id = f'{div_name[:2]}2019'
            try:
                get_div = TM_DIV.objects.get(div_id=div_id,is_deleted=False)
                if not div_org_id and not div_dept_id:
                    get_div.update(div_id=div_id,div_name=div_name,div_dept_id=div_dept_id,
                                   div_org_id=div_org_id,div_desc=div_desc,modified_by=old_token.email)
                else:
                    get_div.update(div_id=div_id,div_name=div_name,modified_by=old_token.email)
                if not new_token:
                    return Response({'success':'DIVISION_DETAILS_UPDATED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'DIVISION_DETAILS_UPDATED','token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
       
                
##############------------for Positions-----------##############

@csrf_exempt
@api_view(["POST"])
def add_post(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            post_name = request.data.get('name')
            post_dept_id = request.data.get('dept_id')
            post_org_id = request.data.get('org_id')
            post_div_id = request.data.get('div_id')
            post_id = f'{post_name[:2]}2019'
            post_add = TM_POST(post_id=post_id,post_name=post_name,
                               post_dept_id=post_dept_id,post_org_id=post_org_id,
                               post_div_id=post_div_id,created_by=old_token.email)
            post_add.save()
            if not new_token:
                return Response({'success':'POSITION_ADDED'},status=HTTP_200_OK)
            else:
                return Response({'success':'POSITION_ADDED','token':new_token},
                                    status=HTTP_200_OK)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["GET"])
def view_post(request,post_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            try:
                get_post = TM_POST.objects.get(post_id=post_id,is_deleted=False)
                if not new_token:
                    return Response({'success':'DIVISION_FOUND','post_data':get_post},status=HTTP_200_OK)
                else:
                    return Response({'success':'DIVISION_FOUND','post_data':get_post,'token':new_token},status=HTTP_200_OK)
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
def del_post(request,post_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_post = TM_POST.objects.get(post_id=post_id,is_deleted=False)
                if not new_token:
                    get_post.soft_delete(old_token.email)
                    return Response({'success':'POSITION_DELETED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'POSITION_DELETED','token':new_token},status=HTTP_200_OK)
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
def update_post(request,post_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            post_name = request.data.get('name')
            post_dept_id = request.data.get('dept_id')
            post_org_id = request.data.get('org_id')
            post_div_id = request.data.get('div_id')
            post_id = f'{post_name[:2]}2019'
            try:
                get_post = TM_POST.objects.get(post_id=post_id,is_deleted=False)
                if not post_org_id and not post_div_id and not post_dept_id:
                    get_post.update(post_id=post_id,post_name=post_name,
                               post_dept_id=post_dept_id,post_org_id=post_org_id,
                               post_div_id=post_div_id,created_by=old_token.email)
                else:
                    get_post.update(post_id=post_id,post_name=post_name,modified_by=old_token.email)
                if not new_token:
                    return Response({'success':'POSITION_DETAILS_UPDATED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'POSITION_DETAILS_UPDATED','token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

############--------for responsibility--------------#################
        
@csrf_exempt
@api_view(["POST"])
def add_resp(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            resp_name = request.data.get('name')
            resp_id = f'{resp_name[:2]}2019'
            resp_desc = request.data.get('desc')
            resp_org_id = request.data.get('org')
            resp_dept_id = request.data.get('dept')
            resp_div_id = request.data.get('div')
            resp_post_id = request.data.get('post')
            resp_user_group_id = request.data.get('user_group')
            resp_add = TM_RESPONSIBILITY(resp_id=resp_id,resp_name=resp_name,resp_org_id=resp_org_id,
                                         resp_desc=resp_desc,resp_dept_id=resp_dept_id,resp_div_id=resp_div_id,
                                         resp_post_id=resp_post_id,resp_user_group_id=resp_user_group_id,
                                         created_by=old_token.email)
            resp_add.save()
            if not new_token:
                return Response({'success':'RESPONSIBILITY_ADDED'},status=HTTP_200_OK)
            else:
                return Response({'success':'RESPONSIBILITY_ADDED','token':new_token},
                                    status=HTTP_200_OK)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["GET"])
def view_resp(request,resp_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            try:
                get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id,is_deleted=False)
                if not new_token:
                    return Response({'success':'RESPONSIBILITY_FOUND','data':get_resp},status=HTTP_200_OK)
                else:
                    return Response({'success':'RESPONSIBILITY_FOUND','data':get_resp,'token':new_token},
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
def del_resp(request,resp_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id,is_deleted=False)
                get_resp.soft_delete(old_token.email)
                if not new_token:
                    return Response({'success':'RESPONSIBILITY_DELETED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'RESPONSIBILITY_DELETED','token':new_token},
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
def updated_resp(request,resp_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            resp_name = request.data.get('name')
            resp_id = f'{resp_name[:2]}2019'
            resp_desc = request.data.get('desc')
            resp_org_id = request.data.get('org')
            resp_dept_id = request.data.get('dept')
            resp_div_id = request.data.get('div')
            resp_post_id = request.data.get('post')
            resp_user_group_id = request.data.get('user_group')
            try:
                get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id,is_deleted=False)
                get_resp.update(resp_id=resp_id,resp_name=resp_name,resp_org_id=resp_org_id,
                                         resp_desc=resp_desc,resp_dept_id=resp_dept_id,resp_div_id=resp_div_id,
                                         resp_post_id=resp_post_id,resp_user_group_id=resp_user_group_id,
                                         modified_by=old_token.email)
                if not new_token:
                    return Response({'success':'RESPONSIBILITY_UPDATED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'RESPONSIBILITY_UPDATED','token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

############------for access views----------##########
        
@csrf_exempt
@api_view(["POST"])
def add_views(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            view_name = request.data.get('name')
            view_id = f'{view_name[:2]}2019'
            view_resp_id = request.data.get('resp')
            view_read_only = False
            view_add = TM_ACCESS_VIEWS(view_id=view_id,view_name=view_name,view_resp_id=view_resp_id,
                                       view_read_only=view_read_only,created_by=old_token.email)
            view_add.save()
            if not new_token:
                return Response({'success':'VIEWS_ADDED'},status=HTTP_200_OK)
            else:
                return Response({'success':'VIEWS_ADDED','token':new_token},
                                    status=HTTP_200_OK)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["GET"])
def view_views(request,view_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,_ = check_token_validity(token)
        if check_token:
            try:
                get_views = TM_ACCESS_VIEWS.objects.get(view_id=view_id,is_deleted=False)
                if not new_token:
                    return Response({'success':'VIEW_FOUND','data':get_views},status=HTTP_200_OK)
                else:
                    return Response({'success':'VIEW_FOUND','data':get_views,'token':new_token},
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
def del_views(request,view_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            try:
                get_views = TM_ACCESS_VIEWS.objects.get(view_id=view_id,is_deleted=False)
                get_views.soft_delete(old_token.email)
                if not new_token:
                    return Response({'success':'VIEW_DELETED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'VIEW_DELETED','token':new_token},
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
def update_views(request,view_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            view_name = request.data.get('name')
            view_id = f'{view_name[:2]}2019'
            view_resp_id = request.data.get('resp')
            view_read_only = False
            try:
                get_views = TM_ACCESS_VIEWS.objects.get(view_id=view_id,is_deleted=False)
                get_views.update(view_id=view_id,view_name=view_name,view_resp_id=view_resp_id,
                                       view_read_only=view_read_only,modified_by=old_token.email)
                if not new_token:
                    return Response({'success':'VIEW_UPDATED'},status=HTTP_200_OK)
                else:
                    return Response({'success':'VIEW_UPDATED','token':new_token},
                                    status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)  
