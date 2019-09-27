from django.db import models 
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)
    status_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(default='',max_length=20)
    created_by = models.CharField(default='',max_length=20)
    
    def soft_delete(self,email):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.status = False
        self.status_at = timezone.now()
        self.modified_by = email
        self.save()
        
    class Meta:
        abstract=True
        

class TM_JOB_REQ_G_INFO(BaseModel):
    job_req_id = models.CharField(primary_key=True,max_length=25)
    job_title = models.CharField(max_length=20)
    job_level = models.CharField(max_length=20)
    job_type = models.CharField(max_length=20)
    job_hire_type = models.CharField(max_length=20)
    job_positions_count = models.PositiveSmallIntegerField()
    job_reason_for_hire = models.CharField(max_length=20)
    job_req_description = models.TextField()
    job_req_resp = models.TextField()
    job_req_qualification = models.TextField()
    job_req_status = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'TM_JOB_REQ_G_INFO'
    
class TM_JOB_REQ_ASSIGN(BaseModel):
    job_assign_id = models.CharField(primary_key=True,max_length=15)
    job_req_id = models.CharField(max_length=25)
    job_hiring_manager = models.CharField(max_length=20)
    job_location = models.CharField(max_length=20)
    job_dept = models.CharField(max_length=20)
    job_div = models.CharField(max_length=20)
    job_recruiter = models.CharField(max_length=20)
    job_reporting_manager = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'TM_JOB_REQ_ASSIGN'
    
class TM_JOB_REQ_APPROVAL_COMMENTS(BaseModel):
    job_approval_comment_id = models.CharField(primary_key=True,max_length=25)
    job_req_id = models.CharField(max_length=25)
    job_req_approval_comment = models.TextField()
    job_req_approval_status = models.CharField(default='',max_length=25)
    
    class Meta:
        db_table = 'TM_JOB_REQ_APPROVAL_COMMENTS'
    

    
    
    
    
        
