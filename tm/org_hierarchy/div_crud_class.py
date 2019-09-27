from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tm_users.models import TM_DIV,TM_ORG,TM_DEPT
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json
from rest_framework.serializers import ModelSerializer


class DivisionSerializer(ModelSerializer):

    class Meta:
        model = TM_DIV
        fields = ('__all__')

class Division_CRUD:
    
    def get_all_div_data(self,request,new_token,old_token):
        div_data = []
        try:
            get_all_div_data_array = TM_DIV.objects.all()
            serialized_queryset_div = serializers.serialize('json', get_all_div_data_array) 
            serialized_queryset_div_json = json.loads(serialized_queryset_div)
            for div in serialized_queryset_div_json:
                org_id = div['fields']['div_org_id']
                dept_id = div['fields']['div_dept_id']
                
                get_org = TM_ORG.objects.get(org_id=org_id)
                get_dept = TM_DEPT.objects.get(dept_id=dept_id)
                
                div_data.append({'id':div['pk'],'addr1':div['fields']['div_desc'],'status':div['fields']['status'],
                                  'name':div['fields']['div_name'],'org':get_org.org_name,'dept':get_dept.dept_name})
            
            if not new_token:
                return Response({'message':'DIV_FOUND','payload':div_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DIV_FOUND','payload':div_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            if not new_token:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
            else:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
    
    def add_div(self,request,new_token,old_token):
        div_name = request.data.get('name')
        div_desc = request.data.get('desc')
        div_org_id = request.data.get('org_id')
        div_dept_id = request.data.get('dept_id')
        div_id = f'{div_org_id[:2]}{div_name[:2]}2019'
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        try:
           get_div = TM_DIV.objects.get(div_id=div_id,div_org_id=div_org_id,div_dept_id=div_dept_id)
           if not new_token:
               return Response({'message':f'{get_div.div_name}_ALREADY_PRESENT','status':HTTP_200_OK},status=HTTP_200_OK)
           else:
                return Response({'message':f'{get_div.div_name}_ALREADY_PRESENT','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except:
            div_add = TM_DIV(div_id=div_id,div_name=div_name,div_dept_id=div_dept_id,div_org_id=div_org_id,div_desc=div_desc,created_by=owner)
            div_add.save()
            if not new_token:
                return Response({'message':'DIVISION_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DIVISION_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        

    def view_div(self,request,div_id,new_token,old_token):
        try:
            get_div = TM_DIV.objects.get(div_id=div_id)
            serialized_queryset_div = serializers.serialize('json', [get_div]) 
            serialized_queryset_div = serialized_queryset_div.strip('[]')
            
            serialized_queryset_div_json = json.loads(serialized_queryset_div)
            org_id = serialized_queryset_div_json['fields']['div_org_id']
            dept_id = serialized_queryset_div_json['fields']['div_dept_id']
            
            get_org = TM_ORG.objects.get(org_id=org_id)
            get_dept = TM_DEPT.objects.get(dept_id=dept_id)
            
            result_json = json.dumps({'id':serialized_queryset_div_json['pk'],'desc':serialized_queryset_div_json['fields']['div_desc'],
                                      'name':serialized_queryset_div_json['fields']['div_name'],     
                                      'status':serialized_queryset_div_json['fields']['status'],'org':get_org.org_name,'dept':get_dept.dept_name})
            
            if not new_token:
                return Response({'message':'DIVISION_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DIVISION_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
    
    
    def del_div(self,request,div_id,new_token,old_token):
        try:
            get_div = TM_DIV.objects.get(div_id=div_id,is_deleted=False)
            if not new_token:
                get_div.soft_delete(old_token.email)
                return Response({'message':'DIVISION_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DIVISION_DELETED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def update_div(self,request,div_id,new_token,old_token):
        div_name = request.data.get('name')
        div_desc = request.data.get('desc')
        div_org_id = request.data.get('org_id')
        div_dept_id = request.data.get('dept_id')
        div_id = f'{div_org_id[:2]}{div_name[:2]}2019'
        try:
            get_div = TM_DIV.objects.get(div_id=div_id)
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_div.created_by
            
            get_div.delete()
            updated_get_div = TM_DIV(div_id=div_id,div_name=div_name,div_dept_id=div_dept_id,
                               div_org_id=div_org_id,div_desc=div_desc,created_by=created_by,modified_by=owner)
            updated_get_div.save()
            if not new_token:
                return Response({'message':'DIVISION_DETAILS_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'DIVISION_DETAILS_UPDATED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        
        
    def get_div_dept_data(self,request,div_dept_id,new_token,old_token):
         try:
            div_array = []
            queryset = TM_DIV.objects.filter(div_dept_id=div_dept_id)
            get_div_data = DivisionSerializer(queryset,many=True).data
            for div in get_div_data:
                div_array.append({'name':div['div_name'],'id':div['div_id']})
            if not new_token:
                return Response({'message':'MEMEBER_FOUND','status':HTTP_200_OK,'payload':div_array},status=HTTP_200_OK)
            else:
                return Response({'message':'MEMEBER_FOUND','token':new_token,'status':HTTP_200_OK,'payload':div_array},status=HTTP_200_OK)
         except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)