from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    token_id = models.CharField(max_length=255)
    email =  models.CharField(max_length=255)
    timestamp = models.DateTimeField(primary_key=True,default=timezone.now)
    
    class Meta:
        abstract=True
        
##To be moved to Redis
class TM_PWD_TOKEN(BaseModel):
    
    class Meta:
        db_table = 'TM_PWD_TOKEN'
        
class TM_USER_TOKEN(BaseModel):
    
    class Meta:
        db_table = 'TM_USER_TOKEN'
        
class TM_JOB_REQ_APPROVAL_TOKEN(BaseModel):
    
    class Meta:
        db_table = 'TM_JOB_REQ_APPROVAL_TOKEN'
    
    
