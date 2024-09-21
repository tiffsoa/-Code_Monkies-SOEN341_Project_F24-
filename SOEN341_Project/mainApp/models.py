from django.db import models

# Create your models here.

# This is where our database tables will go. 

# #This is a table
# class MyUser(models.Model):
#  #This is each collumn of the table
#  username = models.CharField(max_length=255, unique=True)
#  password = models.CharField(max_length=255)

class MyUser(models.Model):  
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    instructor = models.BooleanField(default=False)  


 ##Test
 ## mohammed test