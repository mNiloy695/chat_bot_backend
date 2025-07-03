from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ChatModel(models.Model):
    input_data=models.TextField()
    response_data=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    input_token=models.IntegerField(null=True,blank=True)
    
 
    def __str__(self):
        return f'the created date is : {self.created}'
    class Meta:
        ordering=['-created']

