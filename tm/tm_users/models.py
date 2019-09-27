from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True,auto_now=True)
    status_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(default='',max_length=255)
    created_by = models.CharField(default='',max_length=255)
    
    def soft_delete(self,email):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.status = False
        self.status_at = timezone.now()
        self.modified_by = email
        self.save()
        
    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save(update_fields=kwargs.keys())
    
    class Meta:
        abstract=True

class TM_ORG(BaseModel):
    org_id = models.CharField(primary_key=True,max_length=255)
    org_name = models.CharField(max_length=255)
    org_address = models.CharField(max_length=255)
    org_ext = models.BooleanField()
    org_email = models.CharField(default='dev.skapss@gmail.com',max_length=255)
    
    class Meta:
        db_table = 'TM_ORG'

class TM_DEPT(BaseModel):
    dept_id = models.CharField(primary_key=True,max_length=255)
    dept_name = models.CharField(max_length=255)
    dept_desc = models.CharField(max_length=255)
    dept_org_id = models.CharField(default='',max_length=255)
    
    class Meta:
        db_table = 'TM_DEPT'
        
class TM_DIV(BaseModel):
    div_id = models.CharField(primary_key=True,max_length=255)
    div_name = models.CharField(max_length=255)
    div_desc = models.CharField(max_length=255)
    div_org_id = models.CharField(default='',max_length=255)
    div_dept_id = models.CharField(default='',max_length=255)
    
    class Meta:
        db_table = 'TM_DIV'
    

class TM_POST(BaseModel):
    post_id = models.CharField(primary_key=True,max_length=255)
    post_name = models.CharField(max_length=255)
    post_dept_id = models.CharField(default='',max_length=255)
    post_org_id = models.CharField(default='',max_length=255)
    post_div_id = models.CharField(default='',max_length=255)
    
    class Meta:
        db_table = 'TM_POST'

class TM_USER_GROUP(BaseModel):
    group_id = models.CharField(primary_key=True,max_length=255)
    group_name = models.CharField(max_length=255)
    group_desc = models.CharField(max_length=255)
    group_org_id = models.CharField(default='',max_length=255)
    group_dept_id = models.CharField(default='',max_length=255)
    group_div_id = models.CharField(default='',max_length=255)

    
    class Meta:
        db_table = 'TM_USER_GROUP'
        
class TM_RESPONSIBILITY(BaseModel):
    resp_id = models.CharField(primary_key=True,max_length=255)
    resp_name = models.CharField(max_length=255)
    resp_desc = models.CharField(default='',max_length=255)
    resp_org_id = models.CharField(default='',max_length=255)
    resp_dept_id = models.CharField(default='',max_length=255)
    resp_div_id = models.CharField(default='',max_length=255)
    resp_post_id = models.CharField(default='',max_length=255)
    resp_user_group_id = models.CharField(default='',max_length=255)

    
    class Meta:
        db_table = 'TM_RESPONSIBILITY'
        
class TM_ACCESS_RIGHTS(BaseModel):
    page_id = models.CharField(primary_key=True,max_length=255)
    page_name = models.CharField(max_length=255)
    page_resp_id = models.CharField(default='',max_length=255)
    page_rights_id = models.CharField(default='',max_length=255)

    
    class Meta:
        db_table = 'TM_ACCESS_RIGHTS'
        
class TM_ORG_CONTACT(BaseModel):
    org_cont_id = models.CharField(primary_key=True,max_length=255)
    org_cont_addr2 = models.CharField(max_length=255,null=True,blank=True)
    org_cont_addr3 = models.CharField(max_length=255,null=True,blank=True)
    org_cont_city = models.CharField(max_length=255)
    org_cont_state = models.CharField(max_length=255)
    org_cont_country_code = models.CharField(max_length=255)
    org_cont_zip_code = models.BigIntegerField()
    org_cont_phone = models.BigIntegerField()
    org_id = models.CharField(default='',max_length=255)
    
    class Meta:
        db_table = 'TM_ORG_CONTACT'
        

class TM_USER(BaseModel):
    user_id = models.CharField(primary_key=True,max_length=255)
    username = models.CharField(default='',max_length=255)
    is_active = models.BooleanField(default=True)
    user_addr1 = models.CharField(max_length=255)
    user_dept_id = models.CharField(default='',max_length=255)
    user_div_id = models.CharField(default='',max_length=255)
    user_group_id = models.CharField(default='',max_length=255)
    user_org_id = models.CharField(default='',max_length=255)
    user_post_id = models.CharField(default='',max_length=255)
    user_resp_id = models.CharField(default='',max_length=255)
    user_mobile_num = models.BigIntegerField()
    user_email_id = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'TM_USER'
        
class TM_USER_CONTACT(BaseModel):
    user_cont_id = models.CharField(primary_key=True,max_length=255)
    user_cont_addr2 = models.CharField(max_length=255,null=True,blank=True)
    user_cont_addr3 = models.CharField(max_length=255,null=True,blank=True)
    user_cont_city = models.CharField(max_length=255)
    user_cont_state = models.CharField(max_length=255)
    user_cont_country_code = models.CharField(max_length=255)
    user_cont_zip_code = models.BigIntegerField()
    user_mobile_num2 = models.BigIntegerField(null=True,blank=True)
    user_email_id2 = models.CharField(max_length=255,null=True,blank=True)
    user_id = models.CharField(default='',max_length=255)
    
    class Meta:
        db_table = 'TM_USER_CONTACT'
        
        
class TM_COUNTRY(BaseModel):
    country_id = models.CharField(primary_key=True,max_length=255)
    country_name = models.CharField(max_length=255)
    country_code =  models.CharField(max_length=255)
    
    class Meta:
        db_table = 'TM_COUNTRY'
    
class TM_STATE(BaseModel):
    state_id = models.CharField(primary_key=True,max_length=255)
    state_name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=255)
    state_country_id = models.CharField(default='',max_length=255)
    
    class Meta:
        db_table = 'TM_STATE'
        
class TM_CITY(BaseModel):
    city_id = models.CharField(primary_key=True,max_length=255)
    city_name = models.CharField(max_length=255)
    city_code = models.CharField(max_length=255)
    city_state_id = models.CharField(default='',max_length=255)
    
    class Meta:
        db_table = 'TM_CITY'
