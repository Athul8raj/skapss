from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from tm_users.models import TM_ORG,TM_ORG_CONTACT
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json



class Organization_CRUD:
    
    def get_all_org_data(self,request,new_token,old_token):
        org_data = []
        try:
            get_all_org_data_array = TM_ORG.objects.all()
            serialized_queryset_org = serializers.serialize('json', get_all_org_data_array) 
            serialized_queryset_org_json = json.loads(serialized_queryset_org)
            for org in serialized_queryset_org_json:
                org_data.append({'id':org['pk'],'addr1':org['fields']['org_address'],'status':org['fields']['status'],
                                 'name':org['fields']['org_name'],'email':org['fields']['org_email']})
            if not new_token:
                return Response({'message':'ORG_FOUND','payload':org_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'ORG_FOUND','payload':org_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            if not new_token:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
            else:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
    
    def add_org(self,request,new_token,old_token):
        org_name = request.data.get('name')
        org_address = request.data.get('addr1')
        org_ext = request.data.get('external')
        org_email = request.data.get('email')
        org_id = f'{org_name[:3]}2019'
        status = request.data.get('status')
        org_cont_id = f'{org_name[:3]}ADD2019'
        org_cont_addr2 = request.data.get('address2')
        org_cont_addr3 = request.data.get('address3')
        org_cont_city = request.data.get('city')
        org_cont_state = request.data.get('state')
        org_cont_country_code = request.data.get('country')
        org_cont_zip_code = request.data.get('zip')
        org_cont_phone = request.data.get('phone')
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        try:
            get_org = TM_ORG.objects.get(org_id=org_id)
            if not new_token:
                return Response({'message':f'{get_org.org_name}_ALREADY_PRESENT','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':f'{get_org.org_name}_ALREADY_PRESENT','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except:
            org_add = TM_ORG(org_id=org_id,org_name=org_name,org_address=org_address,status=status,org_email=org_email,org_ext=org_ext,created_by=owner)
            org_contact_add = TM_ORG_CONTACT(org_id=org_id,org_cont_id=org_cont_id,org_cont_addr2=org_cont_addr2,
                                             org_cont_addr3=org_cont_addr3,org_cont_city=org_cont_city,
                                             org_cont_state=org_cont_state,org_cont_country_code=org_cont_country_code,
                                             org_cont_zip_code=org_cont_zip_code,org_cont_phone=org_cont_phone,created_by=owner)
            org_add.save()
            org_contact_add.save()
            if not new_token:
                return Response({'message':f'{org_name.upper()}_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':f'{org_name.upper()}_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)   
    

    def view_org(self,request,org_id,new_token,old_token):
        try:
            get_org = TM_ORG.objects.get(org_id=org_id)
            get_org_contact = TM_ORG_CONTACT.objects.get(org_id=org_id)
            
            serialized_queryset_org = serializers.serialize('json', [get_org]) 
            serialized_queryset_org = serialized_queryset_org.strip('[]')
            serialized_queryset_org_json = json.loads(serialized_queryset_org)            

            serialized_queryset_org_contact = serializers.serialize('json', [get_org_contact]) 
            serialized_queryset_org_contact = serialized_queryset_org_contact.strip('[]')
            serialized_queryset_org_contact_json = json.loads(serialized_queryset_org_contact)
            
            
            result_json = json.dumps({'id':serialized_queryset_org_json['pk'],'addr1':serialized_queryset_org_json['fields']['org_address'],
                             'status':serialized_queryset_org_json['fields']['status'],'name':serialized_queryset_org_json['fields']['org_name'],
                             'email':serialized_queryset_org_json['fields']['org_email'],'phone':serialized_queryset_org_contact_json['fields']['org_cont_phone'],
                             'addr2':serialized_queryset_org_contact_json['fields']['org_cont_addr2'],'addr3':serialized_queryset_org_contact_json['fields']['org_cont_addr3'],
                             'zip':serialized_queryset_org_contact_json['fields']['org_cont_zip_code'],'country':serialized_queryset_org_contact_json['fields']['org_cont_country_code'],
                             'state':serialized_queryset_org_contact_json['fields']['org_cont_state'],'city':serialized_queryset_org_contact_json['fields']['org_cont_city']})

            if not new_token:
                return Response({'message':'ORG_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'ORG_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND2',},status=HTTP_404_NOT_FOUND)
    
    
    def del_org(self,request,org_id,new_token,old_token):
        try:
            get_org = TM_ORG.objects.get(org_id=org_id,is_deleted=False)
            get_org_contact = TM_ORG_CONTACT.objects.get(org_id=org_id,is_deleted=False)
            if not new_token:
                get_org.soft_delete(old_token.email)
                get_org_contact.soft_delete(old_token.email)
                return Response({'message':'ORG_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'ORG_DELETED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def update_org(self,request,org_id,new_token,old_token):
        try:
            get_org = TM_ORG.objects.get(org_id=org_id)
            get_org_contact = TM_ORG_CONTACT.objects.get(org_id=org_id)
            org_name = request.data.get('name')
            org_address = request.data.get('addr1')
            org_ext = request.data.get('external')
            status = request.data.get('status')
            org_id = f'{org_name[:4]}2019'
            org_cont_id = f'{org_name[:3]}ADD2019'
            org_cont_addr2 = request.data.get('addr2')
            org_cont_addr3 = request.data.get('addr3')
            org_cont_city = request.data.get('city')
            org_cont_state = request.data.get('state')
            org_cont_country_code = request.data.get('country')
            org_cont_zip_code = request.data.get('zip')
            org_cont_phone = request.data.get('phone') 
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_org.created_by
            
            get_org.delete()
            get_org_contact.delete()
            updated_get_org = TM_ORG(org_id=org_id,org_name=org_name,org_address=org_address,status=status,
                           org_ext=org_ext,created_by=created_by,modified_by=owner)
            updated_get_org.save()
            updated_get_org_contact = TM_ORG_CONTACT(org_id=org_id,org_cont_id=org_cont_id,org_cont_addr2=org_cont_addr2,
                                     org_cont_addr3=org_cont_addr3,org_cont_city=org_cont_city,
                                     org_cont_state=org_cont_state,org_cont_country_code=org_cont_country_code,
                                     org_cont_zip_code=org_cont_zip_code,org_cont_phone=org_cont_phone,created_by=created_by,modified_by=owner)
            updated_get_org_contact.save()
            if not new_token:
                return Response({'message':'ORG_DETAILS_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'ORG_DETAILS_UPDATED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)