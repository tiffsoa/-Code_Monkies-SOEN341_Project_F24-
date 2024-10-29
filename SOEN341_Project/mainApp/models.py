from django.db import models

# Create your models here.

# This is where our database tables will go. 

class MyUser(models.Model):
    id = models.AutoField(primary_key=True) #each user should have an id in the database
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    instructor = models.BooleanField(default=False)  
