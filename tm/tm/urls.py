from django.contrib import admin
from django.urls import path,include
from rest_framework import routers

from tm_users.views import login
from send_mail.views import pwd_reset_email
from tokens.views import update_pwd

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login),
    path('/',include(router.urls)),
    path('auth/forgot-password/reset-request/<str:email>',pwd_reset_email),
    path('auth/forgot-password/reset-password/<str:token>',update_pwd)    
]
