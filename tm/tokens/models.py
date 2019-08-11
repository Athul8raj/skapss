from django.db import models
from django.utils import timezone


##To be moved to Redis
class TM_PWD_TOKEN(models.Model):
    token_id = models.CharField(max_length=50)
    email =  models.CharField(max_length=50)
    timestamp = models.DateTimeField(primary_key=True,default=timezone.now)
    
    class Meta:
        db_table = 'TM_PWD_TOKEN'
        
class TM_USER_TOKEN(models.Model):
    token_id = models.CharField(max_length=50)
    email =  models.CharField(max_length=50)
    timestamp = models.DateTimeField(primary_key=True)
    
    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()
    
    class Meta:
        db_table = 'TM_USER_TOKEN'
    
    
