from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tm_users.models import TM_USER_GROUP,TM_ORG,TM_DEPT,TM_DIV
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json
from rest_framework.serializers import ModelSerializer


class UserGroupSerializer(ModelSerializer):

    class Meta:
        model = TM_USER_GROUP
        fields = ('__all__')

class UserGroup_CRUD:
    
    def get_all_group_data(self,request,new_token,old_token):
        group_data = []
        try:
            get_all_dept_data_array = TM_USER_GROUP.objects.all()
            serialized_queryset_group = serializers.serialize('json', get_all_dept_data_array)
            serialized_queryset_group_json = json.loads(serialized_queryset_group)
            for group in serialized_queryset_group_json:
                org_id = group['fields']['group_org_id']
                dept_id = group['fields']['group_dept_id']
                
                get_org = TM_ORG.objects.get(org_id=org_id)
                get_dept = TM_DEPT.objects.get(dept_id=dept_id)
                
                
                group_data.append({'id':group['pk'],'desc':group['fields']['group_desc'],'status':group['fields']['status'],
                                  'name':group['fields']['group_name'],'org':get_org.org_name,'dept':get_dept.dept_name,
                                  })
            if not new_token:
                return Response({'message':'USER_GROUP_FOUND','payload':group_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_GROUP_FOUND','payload':group_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            if not new_token:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
            else:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
    
    def add_group(self,request,new_token,old_token):    
        group_name = request.data.get('name')
        group_desc = request.data.get('desc')
        group_org_id = request.data.get('org_id')
        group_dept_id = request.data.get('dept_id')     
        group_id = f'{group_name[:2]}2019'
        status = request.data.get('status')
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        try:
            get_group = TM_USER_GROUP.objects.get(group_id=group_id,group_org_id=group_org_id,group_dept_id=group_dept_id,
                                                  )
            if not new_token:
                return Response({'message':f'{get_group.group_name}_ALREADY_PRESENT','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':f'{get_group.group_name}_ALREADY_PRESENT','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except: 
            group_add = TM_USER_GROUP(group_name=group_name,group_id=group_id,status=status,group_org_id=group_org_id,
                                      group_dept_id=group_dept_id,group_desc=group_desc,
                                      created_by=owner)
            group_add.save()
            if not new_token:
                return Response({'message':'USER_GROUP_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_GROUP_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        

    def view_group(self,request,group_id,new_token,old_token):
        try:
            get_group = TM_USER_GROUP.objects.get(group_id=group_id)
            serialized_queryset_group = serializers.serialize('json', [get_group]) 
            serialized_queryset_group = serialized_queryset_group.strip('[]')
            serialized_queryset_group_json = json.loads(serialized_queryset_group)
            
            result_json = json.dumps({'id':serialized_queryset_group_json['pk'],'desc':serialized_queryset_group_json['fields']['group_desc'],'name':serialized_queryset_group_json['fields']['group_name'],
                             'status':serialized_queryset_group_json['fields']['status'],'org':serialized_queryset_group_json['fields']['group_org_id'],
                             'dept':serialized_queryset_group_json['fields']['group_dept_id']})
            
            if not new_token:
                return Response({'message':'USER_GROUP_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_GROUP_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def del_group(self,request,group_id,new_token,old_token):
        try:
            get_group = TM_USER_GROUP.objects.get(group_id=group_id,is_deleted=False)
            if not new_token:
                get_group.soft_delete(old_token.email)
                return Response({'message':'USER_GROUP_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_GROUP_DELETED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def update_group(self,request,group_id,new_token,old_token):
        group_name = request.data.get('name')
        group_desc = request.data.get('desc')
        group_org_id = request.data.get('org_id')
        group_dept_id = request.data.get('dept_id')
        group_id = f'{group_name[:2]}2019'
        status = request.data.get('status')
        try:
            get_group = TM_USER_GROUP.objects.get(group_id=group_id)
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_group.created_by
            
            get_group.delete()            
            updated_get_group = TM_USER_GROUP(group_name=group_name,group_id=group_id,status=status,group_org_id=group_org_id,
                                             group_dept_id=group_dept_id,
                                             group_desc=group_desc,created_by=created_by,modified_by=owner)
            updated_get_group.save()
            
            if not new_token:
                return Response({'message':'USER_GROUP_DETAILS_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_GROUP_DETAILS_UPDATED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        
    def get_group_div_data(self,request,group_dept_id,new_token,old_token):
         try:
            group_array = []
            queryset = TM_USER_GROUP.objects.filter(group_dept_id=group_dept_id)
            get_group_data = UserGroupSerializer(queryset,many=True).data
            for group in get_group_data:
                group_array.append({'name':group['group_name'],'id':group['group_id']})
            if not new_token:
                return Response({'message':'MEMEBER_FOUND','status':HTTP_200_OK,'payload':group_array},status=HTTP_200_OK)
            else:
                return Response({'message':'MEMEBER_FOUND','token':new_token,'status':HTTP_200_OK,'payload':group_array},status=HTTP_200_OK)
         except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)