from django.urls import path
from .views import *

#These are the url patterns. When user goes to url x, function y in views.py is called. The name is optional, just for clarity.
#this is where we create our url routes then we will connect them to our views

urlpatterns = [
    path('register/', register, name='register'),
    path('/', login_view, name='login'),
    path('instructor/home/', instructor_home_view, name='instructorHomePage'),
    path('student/home/', student_home_view, name='studentHomePage'),

    #path('home/', home_view, name='home'), this is for student home
    #need to add url for instructor home
]