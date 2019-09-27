from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.status import ( HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_405_METHOD_NOT_ALLOWED )
from rest_framework.response import Response
from tokens.token import check_token_validity
from .org_crud_class import Organization_CRUD
from .dept_crud_class import Department_CRUD
from .div_crud_class import Division_CRUD
from .post_crud_class import Position_CRUD
from .user_group_crud_class import UserGroup_CRUD
from .user_crud_class import User_CRUD
from .resp_crud_class import Responsibility_CRUD

               

#########------------for organization------------#########

org_crud_instance = Organization_CRUD()

@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def org_crud(request,org_id=None):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST':
                return org_crud_instance.add_org(request,new_token,old_token)
            if request.method == 'GET' and org_id:
                return org_crud_instance.view_org(request,org_id,new_token,old_token)
            if request.method == 'GET' and not org_id:
                return org_crud_instance.get_all_org_data(request,new_token,old_token)
            elif request.method == 'DELETE':
                return org_crud_instance.del_org(request,org_id,new_token,old_token)
            elif request.method == 'PUT':
                return org_crud_instance.update_org(request,org_id,new_token,old_token)  
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)           
        
        
###########-------for departments----------##########      

dept_crud_instance = Department_CRUD()        
        
@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def dept_crud(request,dept_id=None,dept_org_id=None):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST':
                return dept_crud_instance.add_dept(request,new_token,old_token)
            elif request.method == 'GET' and dept_id:
                return dept_crud_instance.view_dept(request,dept_id,new_token,old_token)
            elif request.method == 'GET' and not dept_id and not dept_org_id:
                return dept_crud_instance.get_all_dept_data(request,new_token,old_token)
            elif request.method == 'GET' and dept_org_id:
                return dept_crud_instance.get_dept_data_from_org_id(request,dept_org_id,new_token,old_token)
            elif request.method == 'DELETE':
                return dept_crud_instance.del_dept(request,dept_id,new_token,old_token)
            elif request.method == 'PUT':
                return dept_crud_instance.update_dept(request,dept_id,new_token,old_token)
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        
        
        
##########---------for Divisions--------##############        

div_crud_instance = Division_CRUD()        

@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def div_crud(request,div_id=None,div_dept_id=None):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST':
                return div_crud_instance.add_div(request,new_token,old_token)
            elif request.method == 'GET' and div_id:
                return div_crud_instance.view_div(request,div_id,new_token,old_token)
            elif request.method == 'GET' and not div_id and not div_dept_id:
                return div_crud_instance.get_all_div_data(request,new_token,old_token)
            elif request.method == 'GET' and div_dept_id:
                return div_crud_instance.get_div_dept_data(request,div_dept_id,new_token,old_token)
            elif request.method == 'DELETE':
                return div_crud_instance.del_div(request,div_id,new_token,old_token)
            elif request.method == 'PUT':
                return div_crud_instance.update_div(request,div_id,new_token,old_token)  
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
       
                
##############------------for Positions-----------##############

post_crud_instance = Position_CRUD()
        
@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def post_crud(request,post_id=None,post_dept_id=None):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST':
                return post_crud_instance.add_post(request,new_token,old_token)
            elif request.method == 'GET' and post_id:
                return post_crud_instance.view_post(request,post_id,new_token,old_token)
            elif request.method == 'GET' and not post_id and not post_dept_id:
                return post_crud_instance.get_all_position_data(request,new_token,old_token)
            elif request.method == 'GET' and  post_dept_id:
                return post_crud_instance.get_post_div_data(request,post_dept_id,new_token,old_token)
            elif request.method == 'DELETE':
                return post_crud_instance.del_post(request,post_id,new_token,old_token)
            elif request.method == 'PUT':
                return post_crud_instance.update_post(request,post_id,new_token,old_token)
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
 
###########----for User Group------#########################
        
user_group_crud_instance = UserGroup_CRUD()

@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def user_group_crud(request,group_id=None,group_dept_id=None):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST':
                return user_group_crud_instance.add_group(request,new_token,old_token)
            elif request.method == 'GET' and group_id:
                return user_group_crud_instance.view_group(request,group_id,new_token,old_token)
            elif request.method == 'GET' and not group_id and not group_dept_id:
                return user_group_crud_instance.get_all_group_data(request,new_token,old_token)
            elif request.method == 'GET' and group_dept_id:
                return user_group_crud_instance.get_group_div_data(request,group_dept_id,new_token,old_token)
            elif request.method == 'DELETE':
                return user_group_crud_instance.del_group(request,group_id,new_token,old_token)
            elif request.method == 'PUT':
                return user_group_crud_instance.update_group(request,group_id,new_token,old_token)
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        
##########---------for User ----------#######

user_crud_instance = User_CRUD()

@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def user_crud(request,user_id=None):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST':
                return user_crud_instance.add_user(request,new_token,old_token)
            if request.method == 'GET' and user_id:
                return user_crud_instance.view_user(request,user_id,new_token,old_token)
            if request.method == 'GET' and not user_id:
                return user_crud_instance.get_all_user_data(request,new_token,old_token)
            elif request.method == 'DELETE':
                return user_crud_instance.del_user(request,user_id,new_token,old_token)
            elif request.method == 'PUT':
                return user_crud_instance.update_user(request,user_id,new_token,old_token)
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

############--------for responsibility--------------#################

resp_crud_instance = Responsibility_CRUD()

@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def resp_crud(request,resp_id=None):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST' and not resp_id:
                return resp_crud_instance.add_resp(request,new_token,old_token)
            if request.method == 'POST' and resp_id:
                return resp_crud_instance.add_rights(request,resp_id,new_token,old_token)
            if request.method == 'GET' and resp_id:
                return resp_crud_instance.view_resp(request,resp_id,new_token,old_token)
            if request.method == 'GET' and not resp_id:
                return resp_crud_instance.get_all_resp_data(request,new_token,old_token)
            elif request.method == 'DELETE':
                return resp_crud_instance.del_resp(request,resp_id,new_token,old_token)
            elif request.method == 'PUT':
                return resp_crud_instance.update_resp(request,resp_id,new_token,old_token)
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)