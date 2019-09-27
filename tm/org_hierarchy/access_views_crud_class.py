from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tm_users.models import TM_ACCESS_VIEWS,TM_RESPONSIBILITY
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json

class AccessViews_CRUD:
    
    def get_all_acc_view_data(self,request,new_token,old_token):
        view_data = []
        try:
            get_all_acc_view_data_array = TM_ACCESS_VIEWS.objects.all()
            serialized_queryset_view = serializers.serialize('json', get_all_acc_view_data_array) 
            serialized_queryset_view_json = json.loads(serialized_queryset_view)
            for view in serialized_queryset_view_json:
                resp_id = view['fields']['view_resp_id']
                get_resp  =TM_RESPONSIBILITY.objects.get(resp_id=resp_id)
                
                view_data.append({'id':view['pk'],'resp_name':get_resp.resp_name,'status':view['fields']['status'],
                                 'name':view['fields']['view_name'],'read-only':view['fields']['view_read_only']})
            
            if not new_token:
                return Response({'message':'ACCESS_VIEWS_FOUND','payload':view_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'ACCESS_VIEWS_FOUND','payload':view_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            if not new_token:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
            else:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
    
    def add_views(self,request,new_token,old_token):
        view_name = request.data.get('name')
        view_id = f'{view_name[:2]}2019'
        view_resp_id = request.data.get('resp_id')        
        view_read_only = False
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        try:
            get_views = TM_ACCESS_VIEWS.objects.get(view_id=view_id,view_resp_id=view_resp_id)
            if not new_token:
                return Response({'message':f'{get_views.view_name}_ALREADY_PRESENT','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':f'{get_views.view_name}_ALREADY_PRESENT','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except:
            view_add = TM_ACCESS_VIEWS(view_id=view_id,view_name=view_name,view_resp_id=view_resp_id,
                                       view_read_only=view_read_only,created_by=owner)
            view_add.save()
            if not new_token:
                return Response({'message':'VIEWS_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'VIEWS_ADDED','token':new_token,'status':HTTP_200_OK},
                                    status=HTTP_200_OK)
        

    def view_views(self,request,view_id,new_token,old_token):
        try:
            get_views = TM_ACCESS_VIEWS.objects.get(view_id=view_id)
            serialized_queryset_view = serializers.serialize('json', [get_views]) 
            serialized_queryset_view = serialized_queryset_view.strip('[]')
            serialized_queryset_view_json = json.loads(serialized_queryset_view) 
            
            resp_id = serialized_queryset_view_json['fields']['view_resp_id']
            get_resp  =TM_RESPONSIBILITY.objects.get(resp_id=resp_id)
            
            result_json = json.dumps({'id':serialized_queryset_view_json['pk'],'resp_name':get_resp.resp_name,
                                      'status':serialized_queryset_view_json['fields']['status'],'name':serialized_queryset_view_json['fields']['view_name'],
                                      'read-only':serialized_queryset_view_json['fields']['view_read_only']})
            
            if not new_token:
                return Response({'message':'VIEW_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'VIEW_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},
                                status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
    
    
    def del_views(self,request,view_id,new_token,old_token):
        try:
            get_views = TM_ACCESS_VIEWS.objects.get(view_id=view_id,is_deleted=False)
            get_views.soft_delete(old_token.email)
            if not new_token:
                return Response({'message':'VIEW_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'VIEW_DELETED','token':new_token,'status':HTTP_200_OK},
                                status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def update_views(self,request,view_id,new_token,old_token):
        view_name = request.data.get('name')
        view_id = f'{view_name[:2]}2019'
        view_resp_id = request.data.get('resp_id')
        view_read_only = False
        try:
            get_views = TM_ACCESS_VIEWS.objects.get(view_id=view_id)
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_views.created_by
            
            get_views.delete()
            updated_get_views = TM_ACCESS_VIEWS(view_id=view_id,view_name=view_name,view_resp_id=view_resp_id,
                                   view_read_only=view_read_only,created_by=created_by,modified_by=owner)
            updated_get_views.save()
            
            if not new_token:
                return Response({'message':'VIEW_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'VIEW_UPDATED','token':new_token,'status':HTTP_200_OK},
                                status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)