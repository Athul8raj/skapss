from django.contrib import admin
from django.urls import path
from tm_users.views import login,update_pwd,logout
from send_mail.views import pwd_reset_email,check_update_pwd_token
from org_hierarchy.views import (org_crud,dept_crud,div_crud,post_crud,user_group_crud,
                                 user_crud,resp_crud)                               
from job_requisition.views import job_req_crud,send_job_req_approval_mail

urlpatterns = [    
############---------for authentication--------------#########
    
    path('admin/', admin.site.urls),
    path('api/login',login),
    path('api/logout',logout),
    path('auth/forgot-password/reset-request/<str:email>',pwd_reset_email),
    path('auth/forgot-password/check-reset-token/<str:token>',check_update_pwd_token),
    path('auth/forgot-password/reset-password/<str:token>',update_pwd),
    
##############------for authorization-----------------#########
    
    path('org',org_crud,{'org_id': None}),
    path('org/<str:org_id>',org_crud),
    
    path('dept',dept_crud,{'dept_id': None}),
    path('dept/org',org_crud,{'org_id': None}),
    path('dept/<str:dept_id>',dept_crud),
    
    path('div',div_crud,{'div_id': None}),
    path('div/org',org_crud,{'org_id': None}),
    path('div/dept/<str:dept_org_id>',dept_crud),
    path('div/<str:div_id>',div_crud),
    
    path('post',post_crud,{'post_id': None}),
    path('post/org',org_crud,{'org_id': None}),
    path('post/dept/<str:dept_org_id>',dept_crud),
    path('post/div/<str:div_dept_id>',div_crud),
    path('post/<str:post_id>',post_crud),

    
    path('group',user_group_crud,{'group_id': None}),
    path('group/org',org_crud,{'org_id': None}),
    path('group/dept/<str:dept_org_id>',dept_crud),
    path('group/div/<str:div_dept_id>',div_crud), 
    path('group/<str:group_id>',user_group_crud),   
    
    path('resp',resp_crud,{'resp_id': None}),
    path('resp/org',org_crud,{'org_id': None}),
    path('resp/dept/<str:dept_org_id>',dept_crud),
    path('resp/group/<str:group_dept_id>',user_group_crud),
    path('resp/rights/<str:resp_id>',resp_crud),    
    path('resp/<str:resp_id>',resp_crud),
    
    path('user',user_crud,{'user_id': None}),
    path('user/org',org_crud,{'org_id': None}),
    path('user/dept/<str:dept_org_id>',dept_crud),
    path('user/div/<div_dept_id>',div_crud),
    path('user/post/<str:post_dept_id>',post_crud),
    path('user/group/<str:group_dept_id>',user_group_crud),
    path('user/resp/<str:resp_group_id>',resp_crud),
    path('user/<str:user_id>',user_crud),  
    

######------for job requisition-------#########
    
    path('requisition',job_req_crud,{'job_req_id':None}),
    path('requisition/approval',send_job_req_approval_mail),
    path('requisition/dept/<str:dept_org_id>',dept_crud,{'dept_org_id':'Ne2019'}),
    path('requisition/manager/<str:user_org_id>',user_crud),
    path('requisition/panel',user_crud,{'user_id': None}),
    path('requisition/recruiter',user_crud,{'user_id': None}),
    path('requisition/<str:job_req_id>',job_req_crud),
    

    
]
