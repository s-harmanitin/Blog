# Create your models here.
from django.db import models
from cloudinary.models import CloudinaryField
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

    
class tag(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title


class blog(models.Model):
    heading = models.CharField(max_length=50)
    image = CloudinaryField('image')
    desc = models.TextField(max_length=1000000)
    upload_on = models.CharField(max_length=50)
    upload_by = models.CharField(max_length=100)
    datefield = models.DateField(auto_now_add=True)
    tag = models.ForeignKey(tag,on_delete=models.CASCADE,null=True)
    
    
    def __str__(self):
        return self.heading
    
class userdetails(models.Model):
    name = models.CharField(max_length=30)
    profileimage = CloudinaryField('image')
    phonenumber = models.PositiveIntegerField()
    
    
    
    
    

