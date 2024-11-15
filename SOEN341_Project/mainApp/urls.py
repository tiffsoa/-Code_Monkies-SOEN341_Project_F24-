from django.urls import path
from .views import *

#These are the url patterns. When user goes to url x, function y in views.py is called. The name is optional, just for clarity.
#this is where we create our url routes then we will connect them to our views

urlpatterns = [
    path('register/', register, name='register'),
    path('', login_view, name='login'),
    path('instructor/home/', instructor_home_view, name='instructorHomePage'),
    path('student/home/', student_home_view, name='studentHomePage'),
    path('student/home/logout', logout, name='logout'),
    path('instructor/home/logout', logout, name='logout'),
    path('instructor/CloseOpenTeam/<int:team_id>', CloseOpenTeam, name='CloseOpenTeam'),
    path('instructor/teamRatings/<int:team_id>', instructorTeamRatings, name='instructorTeamRatings'),
    path('instructor/teamRatingsDownload/<int:team_id>', instructorTeamRatingsDownload, name='instructorTeamRatingsDownload'),
    path('instructor/overallRatings', instructorOverallRatings, name='instructorOverallRatings'),
    path('instructor/overallRatingsDownload', instructorOverallRatingsDownload, name='instructorOverallRatingsDownload'),
    path('student/viewTeam/<int:team_id>', viewTeam, name='viewTeam'),
    path('instructor/viewTeam/<int:team_id>', instructorViewTeam, name='instructorViewTeam'),
    path('student/teamRatings/<int:team_id>', studentTeamRatings, name='studentTeamRatings'),
    path('student/teamRatingsDownload/<int:team_id>', studentTeamRatingsDownload, name='studentTeamRatingsDownload'),
    path('instructor/createGroup/', createGroupPage, name='createGroup'),
    path('student/rateMember/<int:team_id>/<int:teammate_id>', RateTeammate, name='RateTeammate'),
    path('instructor/viewTeam/<int:team_id>/<int:teammate_id>',RemoveStudent, name="RemoveStudent"),
    path('instructor/viewTeam/deleteTeam/<int:team_id>', deleteTeam, name="deleteTeam")
]