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

class MyProjects(models.Model):
    student_id = models.IntegerField()
    project_name = models.CharField(max_length = 255, unique=True)
    open = models.BooleanField(default=False)
    instructor_id = models.IntegerField()

class People_Project(models.Model):
    project_id = models.IntegerField()
    student_id = models.IntegerField()
    rating = models.BooleanField(default=False)

class Ratings(models.Model):
    project_id = models.IntegerField()
    student_creator_id = models.IntegerField()
    student_rater_id = models.IntegerField()
    score_cooperation = models.CharField(max_length=1)
    score_conceptual = models.CharField(max_length=1)
    score_practical = models.CharField(max_length=1)
    score_workethic = models.CharField(max_length=1)
    comment = models.CharField(max_length=255)
