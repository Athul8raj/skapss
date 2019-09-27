from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_405_METHOD_NOT_ALLOWED
)
from rest_framework.response import Response
from tokens.token import check_token_validity
from send_mail.views import send_email,format_mail
from tokens.token import user_token
from tokens.models import TM_JOB_REQ_APPROVAL_TOKEN
from .job_req_crud_class import JobReq_CRUD,JobReqComments_CRUD
import datetime,pytz
from django.contrib.auth.models import User


########---------for Job Requistions-------#########

job_req_crud_instance = JobReq_CRUD()

@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def job_req_crud(request,job_req_id=None):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST':
                return job_req_crud_instance.add_job_req(request,new_token,old_token)
            if request.method == 'GET' and job_req_id:
                return job_req_crud_instance.view_job_req(request,job_req_id,new_token,old_token)
            if request.method == 'GET' and not job_req_id:
                return job_req_crud_instance.get_all_job_req_data(request,new_token,old_token)
            elif request.method == 'DELETE':
                return job_req_crud_instance.del_job_req(request,job_req_id,new_token,old_token)
            elif request.method == 'PUT':
                return job_req_crud_instance.update_job_req(request,job_req_id,new_token,old_token)  
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(["POST"])
def send_job_req_approval_mail(request):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            email = request.data.get('email')
            job_req_position = request.data.get('post')
            get_username = User.objects.get(email=email)
            username = get_username.username
            approval_token = user_token.make_token()
            save_approval_token = TM_JOB_REQ_APPROVAL_TOKEN(email=email,timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.utc),token_id=approval_token)
            save_approval_token.save()
            subject = f'Job Requistion Approval - {job_req_position}'
            approval_url = f'https://tm-ui.herokuapp.com/approve-mail/{approval_token}'
            plain_message, email_from, recipient_list,html_msg = format_mail(email,'approver.html',url= approval_url,name=username)
        
            send_email(subject, plain_message, email_from, recipient_list,html_msg)
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
            

##########------job req comments crud----------############
job_req_comments_crud_instance = JobReqComments_CRUD()

@csrf_exempt
@api_view(["POST","GET","DELETE","PUT"])
def job_req_comments_crud(request,job_req_id):
    token =request.headers.get('Authorization')
    if token:
        check_token,new_token,old_token = check_token_validity(token)
        if check_token:
            if request.method == 'POST':
                return job_req_comments_crud_instance.add_job_req_comments(request,job_req_id,new_token,old_token)
            if request.method == 'GET' and job_req_id:
                return job_req_comments_crud_instance.view_job_req_comments(request,job_req_id,new_token,old_token)
            elif request.method == 'DELETE':
                return job_req_comments_crud_instance.del_job_req_comments(request,job_req_id,new_token,old_token)
            elif request.method == 'PUT':
                return job_req_comments_crud_instance.update_job_req_comments(request,job_req_id,new_token,old_token)  
            else:
                return Response({'error':'METHOD_NOT_ALLOWED','status':HTTP_405_METHOD_NOT_ALLOWED},
                                status=HTTP_405_METHOD_NOT_ALLOWED)            
        else:
            return Response({'error': 'TOKEN_EXPIRED'},
                        status=HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'INVALID_REQUEST'},
                        status=HTTP_400_BAD_REQUEST)
    
    
    
    
    
            