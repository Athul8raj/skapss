from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tm_users.models import TM_DEPT,TM_ORG
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json
from rest_framework.serializers import ModelSerializer


class DeptSerializer(ModelSerializer):

    class Meta:
        model = TM_DEPT
        fields = ('__all__')#('dept_id','dept_name','dept_org_id','dept_desc')

class Department_CRUD:
    
    def get_all_dept_data(self,request,new_token,old_token):
        dept_data = []
        try:
            get_all_dept_data_array = TM_DEPT.objects.all()
            serialized_queryset_dept = serializers.serialize('json', get_all_dept_data_array)
            serialized_queryset_dept_json = json.loads(serialized_queryset_dept)
            for dept in serialized_queryset_dept_json:
                org_id = dept['fields']['dept_org_id']
                get_org = TM_ORG.objects.get(org_id=org_id)
                dept_data.append({'id':dept['pk'],'desc':dept['fields']['dept_desc'],'status':dept['fields']['status'],
                                  'name':dept['fields']['dept_name'],'org_name':get_org.org_name})
            if not new_token:
                return Response({'message':'DEPT_FOUND','payload':dept_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DEPT_FOUND','payload':dept_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            if not new_token:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
            else:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
    
    def add_dept(self,request,new_token,old_token):    
        dept_name = request.data.get('name')
        dept_desc = request.data.get('desc')
        dept_org_id = request.data.get('org_id')
        dept_id = f'{dept_org_id[:2]}{dept_name[:2]}2019'
        status = request.data.get('status')
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        try:
                get_dept = TM_DEPT.objects.get(dept_id=dept_id,dept_org_id=dept_org_id)
                if not new_token:
                    return Response({'message':f'{get_dept.dept_name}_ALREADY_PRESENT','status':HTTP_200_OK},status=HTTP_200_OK)
                else:
                    return Response({'message':f'{get_dept.dept_name}_ALREADY_PRESENT','token':new_token,'status':HTTP_200_OK},
                                status=HTTP_200_OK)
        except:
            dept_add = TM_DEPT(dept_name=dept_name,dept_id=dept_id,status=status,dept_org_id=dept_org_id,dept_desc=dept_desc,created_by=owner)
            dept_add.save()
            if not new_token:
                return Response({'message':'DEPT_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DEPT_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        

    def view_dept(self,request,dept_id,new_token,old_token):
        try:
            get_dept = TM_DEPT.objects.get(dept_id=dept_id)
            serialized_queryset_dept = serializers.serialize('json', [get_dept]) 
            serialized_queryset_dept = serialized_queryset_dept.strip('[]')
            serialized_queryset_dept_json = json.loads(serialized_queryset_dept)
            
            org_id = serialized_queryset_dept_json['fields']['dept_org_id']
            get_org = TM_ORG.objects.get(org_id=org_id)
            
            result_json = json.dumps({'id':serialized_queryset_dept_json['pk'],'name':serialized_queryset_dept_json['fields']['dept_name'],'desc':serialized_queryset_dept_json['fields']['dept_desc'],
                             'status':serialized_queryset_dept_json['fields']['status'],'org_name':get_org.org_name,})
            
            if not new_token:
                return Response({'message':'DEPT_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DEPT_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def del_dept(self,request,dept_id,new_token,old_token):
        try:
            get_dept = TM_DEPT.objects.get(dept_id=dept_id,is_deleted=False)
            if not new_token:
                get_dept.soft_delete(old_token.email)
                return Response({'message':'DEPT_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DEPT_DELETED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def update_dept(self,request,dept_id,new_token,old_token):
        dept_name = request.data.get('name')
        dept_desc = request.data.get('desc')
        dept_org_id = request.data.get('org_id')
        dept_id = f'{dept_org_id[:2]}{dept_name[:2]}2019'
        status = request.data.get('status')
        try:
            get_dept = TM_DEPT.objects.get(dept_id=dept_id)
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_dept.created_by
            
            get_dept.delete()            
            updated_get_dept = TM_DEPT(dept_name=dept_name,dept_id=dept_id,
                            dept_org_id=dept_org_id,dept_desc=dept_desc,status=status,created_by=created_by,modified_by=owner)
            updated_get_dept.save()
            
            if not new_token:
                return Response({'message':'DEPT_DETAILS_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DEPT_DETAILS_UPDATED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        
    def get_dept_data_from_org_id(self,request,dept_org_id,new_token,old_token):
        try:
            dept_array = []
            queryset = TM_DEPT.objects.filter(dept_org_id=dept_org_id)
            get_dept_data = DeptSerializer(queryset,many=True).data
            for dept in get_dept_data:
                dept_array.append({'name':dept['dept_name'], 'id':dept['dept_id']})
            if not new_token:
                return Response({'message':'MEMEBER_FOUND','status':HTTP_200_OK,'payload':dept_array},status=HTTP_200_OK)
            else:
                return Response({'message':'MEMEBER_FOUND','token':new_token,'status':HTTP_200_OK,'payload':dept_array},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)       
        
        
        
        
        