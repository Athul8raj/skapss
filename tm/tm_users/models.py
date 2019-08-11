from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)
    status_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(default='',max_length=20)
    
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
        self.save()
    
    class Meta:
        abstract=True

class TM_ORG(BaseModel):
    org_id = models.CharField(primary_key=True,max_length=15)
    org_name = models.CharField(max_length=30)
    org_address = models.CharField(max_length=40)
    org_ext = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_ORG'

class TM_DEPT(BaseModel):
    dept_id = models.CharField(primary_key=True,max_length=15)
    dept_name = models.CharField(max_length=15)
    dept_desc = models.CharField(max_length=30)
    dept_org_id = models.ForeignKey(TM_ORG,db_column='dept_org_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_DEPT'
        
class TM_DIV(BaseModel):
    div_id = models.CharField(primary_key=True,max_length=15)
    div_name = models.CharField(max_length=15)
    div_desc = models.CharField(max_length=30)
    div_org_id = models.ForeignKey(TM_ORG,db_column='div_org_id',on_delete=models.CASCADE, null=True, editable=False)
    div_dept_id = models.ForeignKey(TM_DEPT,db_column='div_dept_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_DIV'
    

class TM_POST(BaseModel):
    post_id = models.CharField(primary_key=True,max_length=15)
    post_name = models.CharField(max_length=20)
    post_dept_id = models.ForeignKey(TM_DEPT,db_column='post_dept_id',on_delete=models.CASCADE, null=True, editable=False)
    post_org_id = models.ForeignKey(TM_ORG,db_column='post_org_id',on_delete=models.CASCADE, null=True, editable=False)
    post_div_id = models.ForeignKey(TM_DIV,db_column='post_div_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_POST'

class TM_USER_GROUP(BaseModel):
    group_id = models.CharField(primary_key=True,max_length=15)
    group_name = models.CharField(max_length=20)
    group_desc = models.CharField(max_length=20)
    group_org_id = models.ForeignKey(TM_ORG,db_column='group_org_id',on_delete=models.CASCADE, null=True, editable=False)
    group_dept_id = models.ForeignKey(TM_DEPT,db_column='group_dept_id',on_delete=models.CASCADE, null=True, editable=False)
    group_div_id = models.ForeignKey(TM_DIV,db_column='group_div_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')

    
    class Meta:
        db_table = 'TM_USER_GROUP'
        
class TM_RESPONSIBILITY(BaseModel):
    resp_id = models.CharField(primary_key=True,max_length=15)
    resp_name = models.CharField(max_length=15)
    resp_desc = models.CharField(max_length=30)
    resp_org_id = models.ForeignKey(TM_ORG,db_column='resp_org_id',on_delete=models.CASCADE, null=True, editable=False)
    resp_dept_id = models.ForeignKey(TM_DEPT,db_column='resp_dept_id',on_delete=models.CASCADE, null=True, editable=False)
    resp_div_id = models.ForeignKey(TM_DIV,db_column='resp_div_id',on_delete=models.CASCADE, null=True, editable=False)
    resp_post_id = models.ForeignKey(TM_POST,db_column='resp_post_id',on_delete=models.CASCADE, null=True, editable=False)
    resp_user_group_id = models.ForeignKey(TM_USER_GROUP,db_column='resp_user_group_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')

    
    class Meta:
        db_table = 'TM_RESPONSIBILITY'
        
class TM_ACCESS_VIEWS(BaseModel):
    view_id = models.CharField(primary_key=True,max_length=15)
    view_name = models.CharField(max_length=15)
    view_resp_id = models.ForeignKey(TM_RESPONSIBILITY,db_column='view_resp_id',on_delete=models.CASCADE, null=True, editable=False)
    view_read_only = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')

    
    class Meta:
        db_table = 'TM_ACCESS_VIEWS'
        
class TM_ORG_CONTACT(BaseModel):
    org_cont_id = models.CharField(primary_key=True,max_length=20)
    org_cont_addr2 = models.CharField(max_length=20)
    org_cont_addr3 = models.CharField(max_length=20)
    org_cont_city = models.CharField(max_length=20)
    org_cont_state = models.CharField(max_length=20)
    org_cont_country_code = models.CharField(max_length=5)
    org_cont_zip_code = models.BigIntegerField()
    org_cont_phone = models.BigIntegerField()
    org_id = models.ForeignKey(TM_ORG,db_column='org_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_ORG_CONTACT'
        

class TM_USER(BaseModel):
    user_id = models.CharField(primary_key=True,max_length=15)
    username = models.OneToOneField(User,on_delete=models.CASCADE,related_name='%(class)s_username')
    is_active = models.BooleanField(default=True)
    user_addr1 = models.CharField(max_length=20)
    user_dept_id = models.ForeignKey(TM_DEPT,db_column='user_dept_id',on_delete=models.CASCADE, null=True, editable=False)
    user_div_id = models.ForeignKey(TM_DIV,db_column='user_div_id',on_delete=models.CASCADE, null=True, editable=False)
    user_group_id = models.ForeignKey(TM_USER_GROUP,db_column='user_group_id',on_delete=models.CASCADE, null=True, editable=False)
    user_org_id = models.ForeignKey(TM_ORG,db_column='user_org_id',on_delete=models.CASCADE, null=True, editable=False)
    user_post_id = models.ForeignKey(TM_POST,db_column='user_post_id',on_delete=models.CASCADE, null=True, editable=False)
    user_resp_id = models.ForeignKey(TM_RESPONSIBILITY,db_column='user_resp_id',on_delete=models.CASCADE, null=True, editable=False)
    user_mobile_num = models.BigIntegerField()
    user_email_id = models.CharField(max_length=20)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_USER'
        
class TM_USER_CONTACT(BaseModel):
    user_cont_id = models.CharField(primary_key=True,max_length=15)
    user_cont_addr2 = models.CharField(max_length=20)
    user_cont_addr3 = models.CharField(max_length=20)
    user_cont_city = models.CharField(max_length=20)
    user_cont_state = models.CharField(max_length=20)
    user_cont_country_code = models.CharField(max_length=5)
    user_cont_zip_code = models.BigIntegerField()
    user_mobile_num2 = models.BigIntegerField()
    user_email_id2 = models.CharField(max_length=20)
    user_id = models.ForeignKey(TM_USER,db_column='user_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_USER_CONTACT'
        
        
class TM_COUNTRY(BaseModel):
    country_id = models.CharField(primary_key=True,max_length=15)
    country_name = models.CharField(max_length=15)
    country_code =  models.CharField(max_length=5)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_COUNTRY'
    
class TM_STATE(BaseModel):
    state_id = models.CharField(primary_key=True,max_length=15)
    state_name = models.CharField(max_length=15)
    state_code = models.CharField(max_length=5)
    state_country_id = models.ForeignKey(TM_COUNTRY,db_column='state_country_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_STATE'
        
class TM_CITY(BaseModel):
    city_id = models.CharField(primary_key=True,max_length=15)
    city_name = models.CharField(max_length=15)
    city_code = models.CharField(max_length=5)
    city_state_id = models.ForeignKey(TM_STATE,db_column='state_country_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_CITY'
        
class TM_ZIPCODE(BaseModel):
    zipcode_id = models.CharField(primary_key=True,max_length=15)
    zipcode = models.CharField(max_length=5)
    zipcode_city_id = models.ForeignKey(TM_CITY,db_column='state_country_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    
    class Meta:
        db_table = 'TM_ZIPCODE'
