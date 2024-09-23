from django.db import models

# Create your models here.

class MyUser(models.Model):  
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    instructor = models.BooleanField(default=False)  
