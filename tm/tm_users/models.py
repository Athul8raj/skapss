from django.db import models
from .util import get_current_user
from django.contrib.auth.models import User
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract=True

class TM_ORG(BaseModel):
    org_id = models.CharField(primary_key=True,max_length=15)
    org_name = models.CharField(max_length=30)
    org_address = models.CharField(max_length=40)
    org_ext = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_ORG, self).save(*args, **kwargs)
    
    
    class Meta:
        db_table = 'TM_ORG'

class TM_DEPT(BaseModel):
    dept_id = models.CharField(primary_key=True,max_length=15)
    dept_name = models.CharField(max_length=15)
    dept_desc = models.CharField(max_length=30)
    dept_org_id = models.ForeignKey(TM_ORG,db_column='dept_org_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_DEPT, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'TM_DEPT'

class TM_POST(BaseModel):
    post_id = models.CharField(primary_key=True,max_length=15)
    post_name = models.CharField(max_length=20)
    post_dept_id = models.ForeignKey(TM_DEPT,db_column='post_dept_id',on_delete=models.CASCADE, null=True, editable=False)
    post_org_id = models.ForeignKey(TM_ORG,db_column='post_org_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_POST, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'TM_POST'

class TM_USER_GROUP(BaseModel):
    group_id = models.CharField(primary_key=True,max_length=15)
    group_name = models.CharField(max_length=20)
    group_desc = models.CharField(max_length=20)
    group_org_id = models.ForeignKey(TM_ORG,db_column='group_org_id',on_delete=models.CASCADE, null=True, editable=False)
    group_dept_id = models.ForeignKey(TM_DEPT,db_column='group_dept_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_USER_GROUP, self).save(*args, **kwargs)

    
    class Meta:
        db_table = 'TM_USER_GROUP'
        
class TM_RESPONSIBILITY(BaseModel):
    resp_id = models.BigAutoField(primary_key=True)
    resp_name = models.CharField(max_length=15)
    resp_desc = models.CharField(max_length=30)
    resp_org_id = models.ForeignKey(TM_ORG,db_column='resp_org_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_RESPONSIBILITY, self).save(*args, **kwargs)

    
    class Meta:
        db_table = 'TM_RESPONSIBILITY'
        
class TM_ACCESS_VIEWS(BaseModel):
    view_id = models.BigAutoField(primary_key=True)
    view_name = models.CharField(max_length=15)
    view_resp_id = models.ForeignKey(TM_RESPONSIBILITY,db_column='view_resp_id',on_delete=models.CASCADE, null=True, editable=False)
    view_read_only = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_ACCESS_VIEWS, self).save(*args, **kwargs)

    
    class Meta:
        db_table = 'TM_ACCESS_VIEWS'
        
class TM_ORG_CONTACT(BaseModel):
    org_cont_id = models.BigAutoField(primary_key=True)
    org_cont_addr2 = models.CharField(max_length=20)
    org_cont_addr3 = models.CharField(max_length=20)
    org_cont_city = models.CharField(max_length=20)
    org_cont_state = models.CharField(max_length=20)
    org_cont_country_code = models.CharField(max_length=5)
    org_cont_zip_code = models.BigIntegerField()
    org_cont_phone = models.BigIntegerField()
    org_id = models.ForeignKey(TM_ORG,db_column='org_id',on_delete=models.CASCADE, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    modified_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_ORG_CONTACT, self).save(*args, **kwargs)

    
    class Meta:
        db_table = 'TM_ORG_CONTACT'
        

class TM_USER(BaseModel):
    user_id = models.CharField(primary_key=True,max_length=15)
    username = models.OneToOneField(User,on_delete=models.CASCADE,related_name='%(class)s_username')
    password = models.OneToOneField(User,on_delete=models.CASCADE,related_name='%(class)s_password')
    is_active = models.BooleanField(default=True)
    user_addr1 = models.CharField(max_length=20)
    user_dept_id = models.ForeignKey(TM_DEPT,db_column='user_dept_id',on_delete=models.CASCADE, null=True, editable=False)
    user_group_id = models.ForeignKey(TM_USER_GROUP,db_column='user_group_id',on_delete=models.CASCADE, null=True, editable=False)
    user_org_id = models.ForeignKey(TM_ORG,db_column='user_org_id',on_delete=models.CASCADE, null=True, editable=False)
    user_post_id = models.ForeignKey(TM_POST,db_column='user_post_id',on_delete=models.CASCADE, null=True, editable=False)
    user_resp_id = models.ForeignKey(TM_RESPONSIBILITY,db_column='user_resp_id',on_delete=models.CASCADE, null=True, editable=False)
    user_mobile_num = models.BigIntegerField()
    user_email_id = models.CharField(max_length=20)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_created')
    modified_by = models.ForeignKey(User,on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')

    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_USER, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'TM_USER'
        
class TM_USER_CONTACT(BaseModel):
    user_cont_id = models.BigAutoField(primary_key=True)
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
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, editable=False, related_name='%(class)s_modified')
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            self.modified_by = user
            if not self.id:
                self.created_by = user
        super(TM_USER_CONTACT, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'TM_USER_CONTACT'
