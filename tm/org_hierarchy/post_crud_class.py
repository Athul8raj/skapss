from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tm_users.models import TM_POST,TM_DEPT,TM_ORG,TM_DIV
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json
from rest_framework.serializers import ModelSerializer


class PositionSerializer(ModelSerializer):

    class Meta:
        model = TM_POST
        fields = ('__all__')

class Position_CRUD:
    
    def get_all_position_data(self,request,new_token,old_token):
        post_data = []
        try:
            get_all_post_data_array = TM_POST.objects.all()
            serialized_queryset_post = serializers.serialize('json', get_all_post_data_array)
            serialized_queryset_post_json = json.loads(serialized_queryset_post)
            for post in serialized_queryset_post_json:
                org_id = post['fields']['post_org_id']
                dept_id = post['fields']['post_dept_id']
                
                get_org = TM_ORG.objects.get(org_id=org_id)
                get_dept = TM_DEPT.objects.get(dept_id=dept_id)
                
                post_data.append({'id':post['pk'],'dept':get_dept.dept_name,'status':post['fields']['status'],
                                  'name':post['fields']['post_name'],'org':get_org.org_name,})
            if not new_token:
                return Response({'message':'POSITIONS_FOUND','payload':post_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'POTIONS_FOUND','payload':post_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            if not new_token:
                return Response({'error': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
            else:
                return Response({'error': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
    
    def add_post(self,request,new_token,old_token):
        post_name = request.data.get('name')
        post_dept_id = request.data.get('dept_id')
        post_org_id = request.data.get('org_id')
#        post_div_id = request.data.get('div_id')
        
        post_id = f'{post_name[:2]}2019'
        status = request.data.get('status')
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        try:
            get_post = TM_POST.objects.get(post_id=post_id,post_dept_id=post_dept_id,post_org_id=post_org_id)
            if not new_token:
                return Response({'message':f'{get_post.post_name}_ALREADY_PRESENT','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':f'{get_post.post_name}_ALREADY_PRESENT','token':new_token,'status':HTTP_200_OK},
                            status=HTTP_200_OK)
        except:
            post_add = TM_POST(post_id=post_id,post_name=post_name,status=status,
                       post_dept_id=post_dept_id,post_org_id=post_org_id,created_by=owner)
            post_add.save()
            if not new_token:
                return Response({'message':'POSITION_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'POSITION_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        

    def view_post(self,request,post_id,new_token,old_token):
        try:
            get_post = TM_POST.objects.get(post_id=post_id)
            serialized_queryset_post = serializers.serialize('json', [get_post]) 
            serialized_queryset_post = serialized_queryset_post.strip('[]')
            serialized_queryset_post_json = json.loads(serialized_queryset_post)

            org_id = serialized_queryset_post_json['fields']['post_org_id']
            dept_id = serialized_queryset_post_json['fields']['post_dept_id']
            
            get_org = TM_ORG.objects.get(org_id=org_id)
            get_dept = TM_DEPT.objects.get(dept_id=dept_id)
            
            result_json = json.dumps({'id':serialized_queryset_post_json['pk'],'dept':get_dept.dept_name,
                             'status':serialized_queryset_post_json['fields']['status'],
                             'name':serialized_queryset_post_json['fields']['post_name'],'org':get_org.org_name})            
            
            if not new_token:
                return Response({'message':'POSITION_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'POSITION_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def del_post(self,request,post_id,new_token,old_token):
        try:
            get_post = TM_POST.objects.get(post_id=post_id,is_deleted=False)
            if not new_token:
                get_post.soft_delete(old_token.email)
                return Response({'message':'POSITION_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'POSITION_DELETED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
    
    
    def update_post(self,request,post_id,new_token,old_token):
        post_name = request.data.get('name')
        post_dept_id = request.data.get('dept_id')
        post_org_id = request.data.get('org_id')
        
        post_id = f'{post_name[:2]}2019'
        status = request.data.get('status')
        try:
            get_post = TM_POST.objects.get(post_id=post_id)
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_post.created_by
            
            get_post.delete()                
            updated_get_post = TM_POST(post_id=post_id,post_name=post_name,status=status,
                           post_dept_id=post_dept_id,post_org_id=post_org_id,created_by=created_by,modified_by=owner)
            updated_get_post.save()
            
            if not new_token:
                return Response({'message':'POSITION_DETAILS_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'POSITION_DETAILS_UPDATED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        
    def get_post_div_data(self,request,post_dept_id,new_token,old_token):
         try:
            post_array = []
            queryset = TM_POST.objects.filter(post_dept_id=post_dept_id)
            get_post_data = PositionSerializer(queryset,many=True).data
            for post in get_post_data:
                post_array.append({'name':post['post_name'],'id':post['post_id']})
            if not new_token:
                return Response({'message':'MEMEBER_FOUND','status':HTTP_200_OK,'payload':post_array},status=HTTP_200_OK)
            else:
                return Response({'message':'MEMEBER_FOUND','token':new_token,'status':HTTP_200_OK,'payload':post_array},status=HTTP_200_OK)
         except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)