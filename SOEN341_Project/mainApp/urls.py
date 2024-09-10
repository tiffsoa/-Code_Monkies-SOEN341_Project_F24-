from django.urls import path
from .views import *

#These are the url patterns. When user goes to url x, function y in views.py is called. The name is optional, just for clarity.

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'), 
]