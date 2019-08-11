from django.contrib import admin
from django.urls import path,include
from rest_framework import routers

from tm_users.views import login,update_pwd
from send_mail.views import pwd_reset_email,check_update_pwd_token
from org_hierarchy.views import view_org,add_org


router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login',login),
    path('auth/forgot-password/reset-request/<str:email>',pwd_reset_email),
    path('auth/forgot-password/reset-password/<str:token>',check_update_pwd_token),
    path('auth/forgot-password/confirm-password/<str:token>',update_pwd),
    path('org_view/<str:token>',view_org),
    path('org-add',add_org)
]
