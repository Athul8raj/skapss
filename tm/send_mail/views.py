from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from tokens.token import make_random_pwd_token,check_pwd_rest_token
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_email(subject, message, email_from, recipient_list,html_message):
    send_mail(subject, message, email_from, recipient_list,html_message=html_message)

@csrf_exempt
def pwd_reset_email(request,email):
    subject = f'Thank you for registering to our site'
    email = b64decode(email).decode('utf-8')
    token,user = make_random_pwd_token(email)
    if token and user:
        reset_url = f'http://192.168.6.134:8086/auth/forgot-password/reset-password/{token}'
        #message =  f'Please click on below link to change your password.Please Note that the below link will be valid only for 30 mins.\n http://192.168.6.134:3000/auth/forgot-password/reset-password/{token}'    
        html_msg = render_to_string('mail_template.html', {'reset_url': reset_url,'name':user.username})
        plain_message = strip_tags(html_msg) 
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['shabak1989@gmail.com','dev.skapss@gmail.com']
        
        send_email(subject, plain_message, email_from, recipient_list,html_msg)
        
        return JsonResponse({'success':'Mail has been sent','status_code':200})
    else:
        return JsonResponse({'error':'Invalid Email','status_code':404})
    

@csrf_exempt
def check_update_pwd_token(request,token):
    token, _ = check_pwd_rest_token(token)
    if token:
        return JsonResponse({'success':True,'status':200})
    else:
        return JsonResponse({'error':'TOKEN_EXPIRED','status':401})
    