from django.urls import path
from .views import *

#These are the url patterns. When user goes to url x, function y in views.py is called. The name is optional, just for clarity.
#this is where we create our url routes then we will connect them to our views

urlpatterns = [
    path('/home/', instructorHomeView, name='instructorHomePage'),
    path('/home/logout', logout, name='logout'),
    path('/teamRatings/<int:team_id>', instructorTeamRatings, name='instructorTeamRatings'),
    path('/teamRatingsDownload/<int:team_id>', instructorTeamRatingsDownload, name='instructorTeamRatingsDownload'),
    path('/overallRatings', instructorOverallRatings, name='instructorOverallRatings'),
    path('/overallRatingsDownload', instructorOverallRatingsDownload, name='instructorOverallRatingsDownload'),
    path('/viewTeam/<int:team_id>', instructorViewTeam, name='instructorViewTeam'),
    path('/createGroup/', createGroupPage, name='createGroup'),
    path('/viewTeam/<int:team_id>/<int:teammate_id>',RemoveStudent, name="RemoveStudent"),
    path('/viewTeam/deleteTeam/<int:team_id>', deleteTeam, name="deleteTeam")
]