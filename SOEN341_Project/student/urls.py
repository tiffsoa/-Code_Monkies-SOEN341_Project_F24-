from django.urls import path
from .views import *

#These are the url patterns. When user goes to url x, function y in views.py is called. The name is optional, just for clarity.
#this is where we create our url routes then we will connect them to our views

urlpatterns = [
    path('/home/', student_home_view, name='studentHomePage'),
    path('/home/logout', logout, name='logout'),
    path('/viewTeam/<int:team_id>', viewTeam, name='viewTeam'),
    path('/teamRatings/<int:team_id>', studentTeamRatings, name='studentTeamRatings'),
    path('/teamRatingsDownload/<int:team_id>', studentTeamRatingsDownload, name='studentTeamRatingsDownload'),
    path('/rateMember/<int:team_id>/<int:teammate_id>', RateTeammate, name='RateTeammate'),
]