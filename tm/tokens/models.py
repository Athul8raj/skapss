from django.db import models
from django.utils import timezone

class PWD_RESET_TOKEN(models.Model):
    token_id = models.CharField(primary_key=True,max_length=50)
    email =  models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'PWD_RESET_TOKEN'
    
