from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from tokens.token import make_random_token
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode


@shared_task
def send_email(subject, message, email_from, recipient_list):
    send_mail(subject, message, email_from, recipient_list)

@csrf_exempt
def pwd_reset_email(request,email):
    subject = 'Thank you for registering to our site'
    email = b64decode(email).decode('utf-8')
    token = make_random_token(email)
    if token:
        message =  f'Please click on below link to change your password.Please Note that the below link will be valid only for 30 mins.\n http://192.168.6.134:3000/auth/forgot-password/reset-password/{token}'    
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['shabak1989@gmail.com','dev.skapss@gmail.com']
        
        send_email(subject, message, email_from, recipient_list)
        
        return JsonResponse({'success':'Mail has been sent','status_code':200})
    else:
        return JsonResponse({'error':'Invalid Email','status_code':404})
    