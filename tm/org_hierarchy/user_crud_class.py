from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tm_users.models import TM_USER,TM_USER_CONTACT,TM_ORG,TM_DEPT,TM_DIV,TM_POST,TM_USER_GROUP,TM_RESPONSIBILITY
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = TM_USER
        fields = ('__all__')
        
class UserContactSerializer(ModelSerializer):

    class Meta:
        model = TM_USER_CONTACT
        fields = ('__all__')



class User_CRUD:
    
    def get_all_user_data(self,request,new_token,old_token):
        user_data = []
        try:
            get_all_user_data_array = TM_USER.objects.all()
            serialized_queryset_user = serializers.serialize('json', get_all_user_data_array) 
            serialized_queryset_user_json = json.loads(serialized_queryset_user)
            for user in serialized_queryset_user_json:
                org_id = user['fields']['user_org_id']
                dept_id = user['fields']['user_dept_id']
                div_id = user['fields']['user_div_id']
                post_id = user['fields']['user_post_id']
                group_id = user['fields']['user_group_id']
#                resp_id = user['fields']['user_resp_id']
                
                get_org = TM_ORG.objects.get(org_id=org_id)
                get_dept = TM_DEPT.objects.get(dept_id=dept_id)
                get_div = TM_DIV.objects.get(div_id=div_id)
                get_post = TM_POST.objects.get(post_id=post_id)
                get_group = TM_USER_GROUP.objects.get(group_id=group_id)
#                get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id)
                
                user_data.append({'id':user['pk'],'addr1':user['fields']['user_addr1'],'status':user['fields']['status'],
                                 'name':user['fields']['username'],'email':user['fields']['user_email_id'],'org':get_org.org_name,
                                 'dept':get_dept.dept_name,'div':get_div.div_name,
                                 'post':get_post.post_name,'group':get_group.group_name})#'resp':get_resp.resp_name,})
            if not new_token:
                return Response({'message':'USERS_FOUND','payload':user_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USERS_FOUND','payload':user_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            if not new_token:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
            else:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
    
    def add_user(self,request,new_token,old_token):
        username = request.data.get('name')
        user_addr1 = 'Neviton Softech Pvt. Ltd.'#request.data.get('addr1')
        user_org_id = request.data.get('org_id')
        user_dept_id = request.data.get('dept_id')
        user_div_id = request.data.get('div_id')
        user_post_id = request.data.get('post_id')
        user_group_id = request.data.get('group_id')
        user_email_id = f'{username}@gmail.com'#request.data.get('email')       
        user_id = f'{user_org_id[:2]}000{username[:3]}2019'
        status = request.data.get('status')
        user_cont_id = f'{user_org_id[:2]}000{username[:3]}ADD2019'
        user_cont_addr2 = 'ABC'#request.data.get('address2')
        user_cont_addr3 = 'CDF'#request.data.get('address3')
        user_cont_city = 'Bangalore'#request.data.get('city')
        user_cont_state = 'Karnataka'#request.data.get('state')
        user_cont_country_code = '+91'#request.data.get('country')
        user_cont_zip_code = '560070'#request.data.get('zip')
        user_mobile_num = 7855258#request.data.get('phone')
        user_mobile_num2 = 4567899
        user_email_id2 = f'{username}@gmail.com'
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        try:
            get_user = TM_USER.objects.get(user_id=user_id,user_org_id=user_org_id,user_dept_id=user_dept_id,user_div_id=user_div_id)
            if not new_token:
                return Response({'message':f'{get_user.username}_ALREADY_PRESENT','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':f'{get_user.username}_ALREADY_PRESENT','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except:
            user_add = TM_USER(user_id=user_id,username=username,user_addr1=user_addr1,status=status,user_mobile_num=user_mobile_num,user_org_id=user_org_id,
                           user_dept_id=user_dept_id,user_div_id=user_div_id,user_email_id=user_email_id,
                           user_post_id=user_post_id,user_group_id=user_group_id,created_by=owner)
            user_contact_add = TM_USER_CONTACT(user_id=user_id,user_cont_id=user_cont_id,user_cont_addr2=user_cont_addr2,
                                         user_cont_addr3=user_cont_addr3,user_cont_city=user_cont_city,user_mobile_num2=user_mobile_num2,
                                         user_cont_state=user_cont_state,user_cont_country_code=user_cont_country_code,user_email_id2=user_email_id2,
                                         user_cont_zip_code=user_cont_zip_code,created_by=owner)
            auth_user = User(email=user_email_id,username=username)
            auth_user.set_password('random1234')
            
            user_add.save()
            user_contact_add.save()
            auth_user.save()
            if not new_token:
                return Response({'message':'USER_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)   
    

    def view_user(self,request,user_id,new_token,old_token):
        try:
            get_user = TM_USER.objects.get(user_id=user_id)
            get_user_contact = TM_USER_CONTACT.objects.get(user_id=user_id)
            
            serialized_queryset_user = serializers.serialize('json', [get_user]) 
            serialized_queryset_user = serialized_queryset_user.strip('[]')
            serialized_queryset_user_json = json.loads(serialized_queryset_user) 
            
            org_id = serialized_queryset_user_json['fields']['user_org_id']
            dept_id = serialized_queryset_user_json['fields']['user_dept_id']
            div_id = serialized_queryset_user_json['fields']['user_div_id']
            post_id = serialized_queryset_user_json['fields']['user_post_id']
            group_id = serialized_queryset_user_json['fields']['user_group_id']
#            resp_id = serialized_queryset_user_json['fields']['user_resp_id']
            
            get_org = TM_ORG.objects.get(org_id=org_id)
            get_dept = TM_DEPT.objects.get(dept_id=dept_id)
            get_div = TM_DIV.objects.get(div_id=div_id)
            get_post = TM_POST.objects.get(post_id=post_id)
            get_group = TM_USER_GROUP.objects.get(group_id=group_id)
#            get_resp = TM_RESPONSIBILITY.objects.get(resp_id=resp_id)

            serialized_queryset_user_contact = serializers.serialize('json', [get_user_contact]) 
            serialized_queryset_user_contact = serialized_queryset_user_contact.strip('[]')
            serialized_queryset_user_contact_json = json.loads(serialized_queryset_user_contact)
            
            
            result_json = json.dumps({'id':serialized_queryset_user_json['pk'],'addr1':serialized_queryset_user_json['fields']['user_addr1'],
                             'status':serialized_queryset_user_json['fields']['status'],'name':serialized_queryset_user_json['fields']['username'],
                             'email':serialized_queryset_user_json['fields']['user_email_id'],'phone':serialized_queryset_user_json['fields']['user_mobile_num'],
                             'addr2':serialized_queryset_user_contact_json['fields']['user_cont_addr2'],'addr3':serialized_queryset_user_contact_json['fields']['user_cont_addr3'],
                             'zip':serialized_queryset_user_contact_json['fields']['user_cont_zip_code'],'country':serialized_queryset_user_contact_json['fields']['user_cont_country_code'],
                             'state':serialized_queryset_user_contact_json['fields']['user_cont_state'],'city':serialized_queryset_user_contact_json['fields']['user_cont_city'],'org':get_org.org_name,
                             'dept':get_dept.dept_name,'div':get_div.div_name,'post':get_post.post_name,'group':get_group.group_name})

            if not new_token:
                return Response({'message':'USER_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
    
    
    def del_user(self,request,user_id,new_token,old_token):
        try:
            get_org = TM_USER.objects.get(user_id=user_id,is_deleted=False)
            get_org_contact = TM_USER_CONTACT.objects.get(user_id=user_id,is_deleted=False)
            if not new_token:
                get_org.soft_delete(old_token.email)
                get_org_contact.soft_delete(old_token.email)
                return Response({'message':'USER_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_DELETED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def update_user(self,request,user_id,new_token,old_token):
        try:
            get_user = TM_USER.objects.get(user_id=user_id)
            get_user_contact = TM_USER_CONTACT.objects.get(user_id=user_id)
            username = request.data.get('name')
            user_addr1 = 'Neviton Softech Pvt. Ltd.'#request.data.get('addr1')
            user_org_id = request.data.get('org_id')
            user_dept_id = request.data.get('dept_id')
            user_div_id = request.data.get('div_id')
            user_post_id = request.data.get('post_id')
            user_group_id = request.data.get('group_id')
            user_email_id = f'{username}@gmail.com'#request.data.get('email')       
            user_id = f'{user_org_id[:2]}000{username[:3]}2019'
            status = request.data.get('status')
            user_cont_id = f'{user_org_id[:2]}000{username[:3]}ADD2019'
            user_cont_addr2 = 'ABC'#request.data.get('address2')
            user_cont_addr3 = 'CDF'#request.data.get('address3')
            user_cont_city = 'Bangalore'#request.data.get('city')
            user_cont_state = 'Karnataka'#request.data.get('state')
            user_cont_country_code = '+91'#request.data.get('country')
            user_cont_zip_code = '560070'#request.data.get('zip')
            user_mobile_num = 7855258#request.data.get('phone')
            user_mobile_num2 = 4567899
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_user.created_by
            
            get_user.delete()
            get_user_contact.delete()
            
            updated_get_user = TM_USER(user_id=user_id,username=username,user_addr1=user_addr1,status=status,user_mobile_num=user_mobile_num,user_org_id=user_org_id,
                           user_dept_id=user_dept_id,user_div_id=user_div_id,user_email_id=user_email_id,
                           user_post_id=user_post_id,user_group_id=user_group_id,created_by=created_by,modified_by=owner)
            
            updated_get_user_contact = TM_USER_CONTACT(user_id=user_id,user_cont_id=user_cont_id,user_cont_addr2=user_cont_addr2,
                                         user_cont_addr3=user_cont_addr3,user_cont_city=user_cont_city,user_mobile_num2=user_mobile_num2,
                                         user_cont_state=user_cont_state,user_cont_country_code=user_cont_country_code,
                                         user_cont_zip_code=user_cont_zip_code,created_by=created_by,modified_by=owner)
            
            updated_get_user.save()
            updated_get_user_contact.save()
            if not new_token:
                return Response({'message':'USER_DETAILS_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'USER_DETAILS_UPDATED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
        