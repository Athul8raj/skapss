from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import (TM_JOB_REQ_ASSIGN,TM_JOB_REQ_G_INFO,
                     TM_JOB_REQ_APPROVAL_COMMENTS)
from django.core import serializers
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_200_OK,)
import json
from rest_framework.serializers import ModelSerializer

class JobReqCommentsSerializer(ModelSerializer):
    
    class Meta:
        model = TM_JOB_REQ_APPROVAL_COMMENTS
        fields = '__all__'


class JobReq_CRUD:
    
    def get_all_job_req_data(self,request,new_token,old_token):
        job_req_data = []
        try:
            get_all_job_req_data_array = TM_JOB_REQ_G_INFO.objects.all()
            serialized_queryset_job_req = serializers.serialize('json', get_all_job_req_data_array) 
            serialized_queryset_job_req_json = json.loads(serialized_queryset_job_req)
            
            for job_req in serialized_queryset_job_req_json:
                job_req_data.append({'id':job_req['pk'],'title':job_req['fields']['job_title'],'status':job_req['fields']['status'],
                                 'count':job_req['fields']['job_positions_count'],'type':job_req['fields']['job_type'],
                                 'reason':job_req['fields']['job_reason_for_hire'],'desc':job_req['fields']['job_req_description'],
                                 'resp':job_req['fields']['job_req_resp'],'qual':job_req['fields']['job_req_qualification'],
                                 'req_status':job_req['fields']['job_req_status']})
            if not new_token:
                return Response({'message':'ORG_FOUND','payload':job_req_data,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'ORG_FOUND','payload':job_req_data,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            if not new_token:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'status':HTTP_200_OK},status=HTTP_200_OK) 
            else:
                return Response({'message': 'MEMEBER_NOT_FOUND','payload': [],'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
            
            
    def add_job_req(self,request,new_token,old_token):
        job_title = request.data.get('title')
        job_level = request.data.get('level')
        job_type = request.data.get('type')
        job_hire_type = request.data.get('hire_type')
        job_positions_count = request.data.get('count')
        job_reason_for_hire = request.data.get('reason')
        job_req_description = request.data.get('desc')
        job_req_resp = request.data.get('resp')
        job_req_qualification = request.data.get('qual')
        job_req_status = request.data.get('req_status')
        status = request.data.get('status')        
        job_hiring_manager = request.data.get('hire_manager')
        job_location = request.data.get('loc')
        job_dept = request.data.get('dept_name')
        job_div = request.data.get('div_name')
        job_recruiter = request.data.get('recruiter')
        job_reporting_manager = request.data.get('report_manager')
        
        job_req_id = f'{job_dept}-{job_div[:2]}-2019'
        job_assign_id = job_req_id
        
        if not new_token:
            owner = old_token.email
        else:
            owner = new_token.email
        job_req_add = TM_JOB_REQ_G_INFO(job_req_id=job_req_id,job_title=job_title,job_level=job_level,job_positions_count=job_positions_count,
                                    status=status,job_type=job_type,job_hire_type=job_hire_type,job_reason_for_hire=job_reason_for_hire,
                                    job_req_description=job_req_description,job_req_resp=job_req_resp,
                                    job_req_qualification=job_req_qualification,job_req_status=job_req_status,created_by=owner)
        job_req_addi_add = TM_JOB_REQ_ASSIGN(job_req_id=job_req_id,job_assign_id=job_assign_id,job_hiring_manager=job_hiring_manager,
                                         job_location=job_location,job_dept=job_dept,job_div=job_div,job_recruiter=job_recruiter,
                                         job_reporting_manager=job_reporting_manager,created_by=owner)
        job_req_add.save()
        job_req_addi_add.save()
        if not new_token:
            return Response({'message':'JOB_REQ_ADDED','status':HTTP_200_OK},status=HTTP_200_OK)
        else:
            return Response({'message':'JOB_REQ_ADDED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)   
    

    def view_job_req(self,request,job_req_id,new_token,old_token):
        try:
            get_job_req = TM_JOB_REQ_G_INFO.objects.get(job_req_id=job_req_id)
            get_job_req_addi = TM_JOB_REQ_ASSIGN.objects.get(job_req_id=job_req_id)
            
            serialized_queryset_job_req = serializers.serialize('json', [get_job_req]) 
            serialized_queryset_job_req = serialized_queryset_job_req.strip('[]')
            serialized_queryset_job_req_json = json.loads(serialized_queryset_job_req)            

            serialized_queryset_job_req_addi = serializers.serialize('json', [get_job_req_addi]) 
            serialized_queryset_job_req_addi = serialized_queryset_job_req_addi.strip('[]')
            serialized_queryset_job_req_addi_json = json.loads(serialized_queryset_job_req_addi)
            
            comments = self.view_job_req_comments(job_req_id)
            if comments:
                comments = comments.job_req_approval_comment
            else:
                comments = None
            
            
            result_json = json.dumps({'id':serialized_queryset_job_req_json['pk'],'title':serialized_queryset_job_req_json['fields']['job_title'],
                                      'status':serialized_queryset_job_req_json['fields']['status'],'count':serialized_queryset_job_req_json['fields']['job_positions_count'],
                                      'type':serialized_queryset_job_req_json['fields']['job_type'],
                                      'reason':serialized_queryset_job_req_json['fields']['job_reason_for_hire'],'desc':serialized_queryset_job_req_json['fields']['job_req_description'],
                                      'resp':serialized_queryset_job_req_json['fields']['job_req_resp'],'qual':serialized_queryset_job_req_json['fields']['job_req_qualification'],
                                      'req_status':serialized_queryset_job_req_json['fields']['job_req_status'],'hire_manager':serialized_queryset_job_req_addi_json['fields']['job_hiring_manager'],
                                      'loc':serialized_queryset_job_req_addi_json['fields']['job_location'],'comments':comments,
                                      'dept_name':serialized_queryset_job_req_addi_json['fields']['job_dept'],'div_name':serialized_queryset_job_req_addi_json['fields']['job_div'],
                                      'recruiter':serialized_queryset_job_req_addi_json['fields']['job_recruiter'],'report_manager':serialized_queryset_job_req_addi_json['fields']['job_reporting_manager']})

            if not new_token:
                return Response({'message':'JOB_REQ_FOUND','payload':json.loads(result_json),'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'JOB_REQ_FOUND','payload':json.loads(result_json),'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMEBER_NOT_FOUND2',},status=HTTP_404_NOT_FOUND)
    
    
    def del_job_req(self,request,job_req_id,new_token,old_token):
        try:
            get_job_req = TM_JOB_REQ_G_INFO.objects.get(job_req_id=job_req_id,is_deleted=False)
            get_job_req_addi = TM_JOB_REQ_ASSIGN.objects.get(job_req_id=job_req_id,is_deleted=False)
            if not new_token:
                get_job_req.soft_delete(old_token.email)
                get_job_req_addi.soft_delete(old_token.email)
                return Response({'message':'JOB_REQ_DELETED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'JOB_REQ_DELETED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
            
    
    def update_job_req(self,request,job_req_id,new_token,old_token):
        try:
            get_job_req = TM_JOB_REQ_G_INFO.objects.get(job_req_id=job_req_id)
            get_job_req_addi = TM_JOB_REQ_ASSIGN.objects.get(job_req_id=job_req_id)
            job_title = request.data.get('title')
            job_level = request.data.get('level')
            job_type = request.data.get('type')
            job_hire_type = request.data.get('hire_type')
            job_positions_count = request.data.get('count')
            job_reason_for_hire = request.data.get('reason')
            job_req_description = request.data.get('desc')
            job_req_resp = request.data.get('resp')
            job_req_qualification = request.data.get('qual')
            job_req_status = request.data.get('req_status')
            status = request.data.get('status')        
            job_hiring_manager = request.data.get('hire_manager')
            job_location = request.data.get('loc')
            job_dept = request.data.get('dept_name')
            job_div = request.data.get('div_name')
            job_recruiter = request.data.get('recruiter')
            job_reporting_manager = request.data.get('report_manager')
        
            job_req_id = f'{job_dept}-{job_div[:2]}-2019'
            job_assign_id = job_req_id
            if not new_token:
                owner = old_token.email
            else:
                owner = new_token.email
            created_by = get_job_req.created_by
            
            get_job_req.delete()
            get_job_req_addi.delete()
            updated_job_req = TM_JOB_REQ_G_INFO(job_req_id=job_req_id,job_title=job_title,job_level=job_level,job_positions_count=job_positions_count,
                                    status=status,job_type=job_type,job_hire_type=job_hire_type,job_reason_for_hire=job_reason_for_hire,
                                    job_req_description=job_req_description,job_req_resp=job_req_resp,
                                    job_req_qualification=job_req_qualification,job_req_status=job_req_status,created_by=created_by,modified_by=owner)
            updated_job_req.save()
            updated_job_req_addi = TM_JOB_REQ_ASSIGN(job_req_id=job_req_id,job_assign_id=job_assign_id,job_hiring_manager=job_hiring_manager,
                                         job_location=job_location,job_dept=job_dept,job_div=job_div,job_recruiter=job_recruiter,
                                         job_reporting_manager=job_reporting_manager,created_by=created_by,modified_by=owner)
            updated_job_req_addi.save()
            if not new_token:
                return Response({'message':'JOB_REQ_DETAILS_UPDATED','status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'JOB_REQ_DETAILS_UPDATED','token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND',},status=HTTP_404_NOT_FOUND)
    

class JobReqComments_CRUD:

    def add_job_req_comments(self,request,job_req_id,new_token,old_token):
        name = request.data.get('name')
        comments = request.data.get('comment')
        job_req_comment_status = request.data.get('job_req_comment_status')
        
        
    def view_job_req_comments(self,request,job_req_id,new_token,old_token):
        comments_array = []
        try:
            get_job_req_comments = TM_JOB_REQ_APPROVAL_COMMENTS.objects.filter(job_req_id=job_req_id)
            serializer_data = JobReqCommentsSerializer(get_job_req_comments,many=True).data
            for comment in serializer_data:
                comments_array.append({'name':comment['created_by'],'comment':comment['job_req_approval_comment'],'job_req_comment_status':comment['job_req_approval_status']})
            if not new_token:
                return Response({'message':'JOB_REQ_COMMENTS_DETAILS','payload':comments_array,'status':HTTP_200_OK},status=HTTP_200_OK)
            else:
                return Response({'message':'JOB_REQ_COMMENTS_DETAILS','payload':comments_array,'token':new_token,'status':HTTP_200_OK},status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'MEMBER_NOT_FOUND','status':HTTP_200_OK,'payload':[]},status=HTTP_200_OK)
            
            