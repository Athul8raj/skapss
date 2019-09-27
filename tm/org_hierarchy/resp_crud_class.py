from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tm_users.models import (TM_RESPONSIBILITY,TM_ORG,TM_DEPT,TM_USER_GROUP,TM_ACCESS_RIGHTS)
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json
from rest_framework.serializers import ModelSerializer


class RepsonsibilitySerializer(ModelSerializer):

    class Meta:
        model = TM_RESPONSIBILITY
        fields = ('__all__')
        
class AccessRightSerializer(ModelSerializer):

    class Meta:
        model = TM_ACCESS_RIGHTS
        fields = ('__all__')
        
def change_index_to_access_right(rights_int_array):
    rights_id = list(map(int,rights_int_array))
    from collections import defaultdict
    rights_string_array = defaultdict(list)
    access_rights_dict = {13: 'CREATE', 12: 'VIEW', 14: 'EDIT', 15: 'DELETE', 18: 'SHARE', 16: 'APPROVE',17: 'REJECT'}
    for k,v in access_rights_dict.items():
        if k in rights_id:
            rights_string_array[v] = [k,True]
        else:
            rights_string_array[v] = [k,False]
    
    return  rights_string_array
 
class Responsibility_CRUD:
    
    def get_all_resp_data(self,request,new_token,old_token):
        resp_data = []
        try:
            get_all_resp_data_array = TM_RESPONSIBILITY.objects.all()
            serialized_queryset_resp = serializers.serialize('json', get_all_resp_data_array) 
            serialized_queryset_resp_json = json.loads(serialized_queryset_resp)
            for resp in serialized_queryset_resp_json:
                org_id = resp['fields']['resp_org_id']
                dept_id = resp['fields']['resp_dept_id']
                group_id = resp['fields']['resp_user_group_id']
                
                get_org = TM_ORG.objects.get(org_id=org_id)
                get_dept = TM_DEPT.objects.get(dept_id=dept_id)
                get_group = TM_USER_GROUP.objects.get(group_id=group_id)
                
                resp_data.append({'id':resp['pk'],'desc':resp['fields']['resp_desc'],'status':resp['fields']['status'],
                                  'name':resp['fields']['resp_name'],'org':get_org.org_name,'dept':get_dept.dept_name,
                                  'group':get_group.group_name})            
            if not new_token:
                return Response({'message':'RESP_FOUND','payload':resp_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'RESP_FOUND','payload':resp_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
           if not new_token:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
           else:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
    
    def add_resp(self,request,new_token,old_token):
        resp_name = request.data.get('name')
        resp_id = f'{resp_name[:2]}2019'
        resp_desc = request.data.get('desc')
        resp_org_id = request.data.get('org_id')
        resp_dept_id = request.data.get('dept_id')
        resp_user_group_id = request.data.get('group_id')        
        status = request.data.get('status')
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        try:
            get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id,resp_org_id=resp_org_id,resp_dept_id=resp_dept_id)
            if not new_token:
                return Response({'message':f'{get_resp.resp_name}_ALREADY_PRESENT','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':f'{get_resp.resp_name}_ALREADY_PRESENT','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except:
            resp_add = TM_RESPONSIBILITY(resp_id=resp_id,resp_name=resp_name,resp_org_id=resp_org_id,status=status,
                                         resp_desc=resp_desc,resp_dept_id=resp_dept_id,
                                         resp_user_group_id=resp_user_group_id,created_by=owner)
            resp_add.save()
            if not new_token:
                return Response({'message':'RESPONSIBILITY_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'RESPONSIBILITY_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        

    def view_resp(self,request,resp_id,new_token,old_token):
        rights_array =[]
        try:
            get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id)
            get_access_rights = TM_ACCESS_RIGHTS.objects.filter(page_resp_id=resp_id)
            get_access_rights_data = AccessRightSerializer(get_access_rights,many=True).data
            
            serialized_queryset_resp = serializers.serialize('json', [get_resp]) 
            serialized_queryset_resp = serialized_queryset_resp.strip('[]')
            serialized_queryset_resp_json = json.loads(serialized_queryset_resp)

            
            org_id = serialized_queryset_resp_json['fields']['resp_org_id']
            dept_id = serialized_queryset_resp_json['fields']['resp_dept_id']
            group_id = serialized_queryset_resp_json['fields']['resp_user_group_id']
            
            get_org = TM_ORG.objects.get(org_id=org_id)
            get_dept = TM_DEPT.objects.get(dept_id=dept_id)
            get_group = TM_USER_GROUP.objects.get(group_id=group_id)
            
            for right in get_access_rights_data:
                rights = change_index_to_access_right(right['page_rights_id'])             
                
                rights_array.append({'page_name':right['page_name'],'page_id':right['page_id'],'rights':rights})
            
            result_json = json.dumps({'id':serialized_queryset_resp_json['pk'],'status':serialized_queryset_resp_json['fields']['status'],
                                      'name':serialized_queryset_resp_json['fields']['resp_name'],'org':get_org.org_name,'dept':get_dept.dept_name,
                                      'group':get_group.group_name,'desc':serialized_queryset_resp_json['fields']['resp_desc'],'rights':rights_array})
            if not new_token:
                return Response({'message':'RESPONSIBILITY_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'RESPONSIBILITY_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},
                                status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def del_resp(self,request,resp_id,new_token,old_token):
        try:
            get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id,is_deleted=False)
            get_rights = TM_ACCESS_RIGHTS.objects.filter(page_resp_id=resp_id)
            get_resp.soft_delete(old_token.email)
            get_rights.soft_delete(old_token.email)
            if not new_token:
                return Response({'message':'RESPONSIBILITY_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'RESPONSIBILITY_DELETED','token':new_token,'status':HTTP_200_OK},
                                status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def update_resp(self,request,resp_id,new_token,old_token):
        resp_name = request.data.get('name')
        resp_id = f'{resp_name[:2]}2019'
        resp_desc = request.data.get('desc')
        resp_org_id = request.data.get('org_id')
        resp_dept_id = request.data.get('dept_id')
        resp_user_group_id = request.data.get('group_id')        
        status = request.data.get('status')
        page_id = request.data.get('page_id')
        page_name = request.data.get('page_name')
        page_rights_id = request.data.get('page_rights_id')
        page_rights_id = ','.join(map(str,page_rights_id))
        try:
            get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id)
            try:
                get_access_rights = TM_ACCESS_RIGHTS.objects.filter(page_resp_id=resp_id)
                get_access_rights.delete()
            except ObjectDoesNotExist:
                pass
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_resp.created_by
            
            get_resp.delete()            
            updated_get_resp = TM_RESPONSIBILITY(resp_id=resp_id,resp_name=resp_name,resp_org_id=resp_org_id,
                                     resp_desc=resp_desc,resp_dept_id=resp_dept_id,resp_user_group_id=resp_user_group_id,
                                     status=status,created_by=created_by,modified_by=owner)
            updated_get_access_rights = TM_ACCESS_RIGHTS(page_resp_id=resp_id,page_name=page_name,page_id=page_id,
                                          page_rights_id=page_rights_id,created_by=created_by,modified_by=owner)
            updated_get_access_rights.save()
            updated_get_resp.save()
            if not new_token:
                return Response({'message':'RESPONSIBILITY_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'RESPONSIBILITY_UPDATED','token':new_token,'status':HTTP_200_OK},
                                status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        
    def add_rights(self,request,resp_id,new_token,old_token):
        page_id = request.data.get('page_id')
        page_name = request.data.get('page_name')
        page_rights_id = request.data.get('page_rights_id')
        page_rights_id = ','.join(map(str,page_rights_id)) ## storing the index_rights as a single string sep-by comma
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        rights_add = TM_ACCESS_RIGHTS(page_resp_id=resp_id,page_name=page_name,page_id=page_id,
                                          page_rights_id=page_rights_id,created_by=owner)        
        rights_add.save()
        if not new_token:
            return Response({'message':'RIGHTS_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
        else:
            return Response({'message':'RIGHTS_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        
        
    def get_resp_group_data(self,request,resp_group_id,new_token,old_token):
         try:
            resp_array = []
            queryset = TM_RESPONSIBILITY.objects.filter(resp_user_group_id=resp_group_id)
            get_resp_data = RepsonsibilitySerializer(queryset,many=True).data
            for resp in get_resp_data:
                resp_array.append({'name':resp['resp_name'],'id':resp['resp_id']})
            if not new_token:
                return Response({'message':'MEMEBER_FOUND','status':HTTP_200_OK,'payload':resp_array},status=HTTP_200_OK)
            else:
                return Response({'message':'MEMEBER_FOUND','token':new_token,'status':HTTP_200_OK,'payload':resp_array},status=HTTP_200_OK)
         except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)