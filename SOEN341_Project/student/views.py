from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import csv
from userAuth.models import *

#this is the main file we will work on
#here, we will create different views or routes that we can access on our website

#This page has all the functions whose job is to return an HTML page when executed.
#Note that all variables which we want to keep attributed to a certain user is saved in the dictionary "session" https://reintech.io/blog/working-with-sessions-in-django-tutorial

def student_home_view(request):
    # Step 1: Retrieve the user ID from session
    user_id = request.session.get('user_id')
    
    # Step 1: Query the Projects_to_Student_Relationships table for the projects the user is in
    user_projects = Projects_to_Student_Relationships.objects.filter(student_id=user_id)
    
    # Step 3: For each project, get project info and instructor details
    projects_info = []
    for user_project in user_projects:
        projectID = user_project.project_id  #Get the unique ID of the project
        instructorID= Projects.objects.get(id=projectID).instructor_id #Get the ID of the instructor
        
        # Get the project details
        project_data = {
            'project_id': projectID,
            'project_name': Projects.objects.get(id=projectID).project_name,
            'instructor_name': MyUser.objects.get(id=instructorID).name
        }
        projects_info.append(project_data)
    
    
    # Now, we have a list with dictionaries sent to the frontend. It looks something like this:
    # [{project_id:123123,project_name:"Some name",is_open:1, instructor_name: "John"}, {project_id:9345353,project_name:"Some other name",is_open:0, instructor_name: "Jane"}]
    # Step 4: Render the information to the template
    return render(request, 'student/homepagestudent.html', {'projects': projects_info})

def viewTeam(request, team_id):
    user_id = request.session.get('user_id')  # get logged-in user's ID from session

    teamName = Projects.objects.get(id = team_id).project_name # get team name

    # Find all students on the team (project) with the given team number
    team_memberships = Projects_to_Student_Relationships.objects.filter(project_id=team_id)

    # Extract the student details for each membership
    student_list = []
    for membership in team_memberships:
        student = MyUser.objects.get(id=membership.student_id)

        #omit the student who's currently viewing from the list
        if student.id == user_id:
            continue
        
        student_list.append({student.name: student.id})

    # Pass the student list to the front-end (in a list of maps)
    context = {'students': student_list, 'teamName': teamName, 'teamID': team_id}
    #i.e. context looks something like {'students':["name1":id1,"name2":id2,"name3",id3]}
    return render(request, 'student/students_in_team.html', context) ### NEED TO MODIFY STUDENTS_IN_TEAM DEPENDING ON THE NAME THE FRONTEND GIVES THE PAGE

def studentTeamRatings(request, team_id):
    #given a student on this page, compile all results for student n from all the members in their team. If a teammate hasn't 
    #rated them yet, include them in list anyway but leave key blank for each value
    
    user_id = request.session.get('user_id')
    student = MyUser.objects.get(id=user_id)
    
    #get teammates'ratings for the student for this team
    ratings = TeamRatings.objects.filter(team_id=team_id, rated_id=user_id)
    
    #get all teammates in team
    teammate_ids = Projects_to_Student_Relationships.objects.filter(project_id=team_id).values_list('student_id', flat=True).distinct()
    
    #list of results
    ratings_list = []
    
    for teammate_id in teammate_ids:
        if teammate_id==user_id:
            continue
        
        teammate = MyUser.objects.get(id=teammate_id)
        
        rating = ratings.filter(rater_id=teammate_id).first()
        

        #data for each teammate
        rating_data = {
            "Name": teammate.username,
            "Cooperation": rating.score_cooperation if rating else None,
            "conceptual": rating.score_conceptual if rating else None,
            "Practical": rating.score_practical if rating else None,
            "work_ethic": rating.score_workethic if rating else None,
            "comments": rating.comment if rating else "",
        }
        
        #calculate average score
        if rating:
            rating_values = [
                rating.score_cooperation,
                rating.score_conceptual,
                rating.score_practical,
                rating.score_workethic
            ]
            
            rating_data["average_across_all"] = sum(rating_values) / len(rating_values)
            
        else:
            rating_data["average_across_all"] = None
            
        #add to the main list
        ratings_list.append(rating_data)
    
    return render(request, 'student/studentTeamRatings.html', {'team_id': team_id,'ratings':ratings_list})

def studentTeamRatingsDownload(request, team_id):
    #current user's id
    current_user_id = request.session.get('user_id')
    
    # CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="ratings_for_{MyUser.objects.get(id=current_user_id).name}.csv"'
    
    # CSV writer + headers
    writer = csv.writer(response)
    writer.writerow(['Teammate Name', 'Cooperation', 'Conceptual', 'Practical', 'Work Ethic', 'Comments', 'Average Score'])

    #fetching ratings that teammates gave to current user in this specific team
    ratings = TeamRatings.objects.filter(team_id=team_id, rated_id=current_user_id).exclude(rater_id=current_user_id)
    
    #lists to store scores + comments
    cooperation, conceptual, practical, work_ethic, comments = [], [], [], [], []
    
    #process ratings
    for rating in ratings:
        #store scores and comments
        cooperation.append(rating.score_cooperation)
        conceptual.append(rating.score_conceptual)
        practical.append(rating.score_practical)
        work_ethic.append(rating.score_workethic)
        if rating.comment:
            comments.append(rating.comment)
            
    #calculate averages
    avg_cooperation = sum(cooperation) / len(cooperation) if cooperation else 0
    avg_conceptual = sum(conceptual) / len(conceptual) if conceptual else 0
    avg_practical = sum(practical) / len(practical) if practical else 0
    avg_work_ethic = sum(work_ethic) / len(work_ethic) if work_ethic else 0
    overall_avg = (avg_cooperation + avg_conceptual + avg_practical + avg_work_ethic) / 4 if ratings else 0
    
    #put all comments in a string
    all_comments = " | ".join(comments) if comments else "No comments"
    
    #write everything in a row
    writer.writerow([
        "Anonymous",
        avg_cooperation,
        avg_conceptual,
        avg_practical,
        avg_work_ethic,
        all_comments,
        overall_avg
    ])
    
    #return response since it's a file download
    return response
       

def RateTeammate(request, team_id, teammate_id): #Mohammed part 
    user_id = request.session.get('user_id')
    
    # Step 1: Check if the user is logged in
    if not user_id:
        return redirect('login')
    
    # Step 2: Check if the student has already rated the teammate for the specified team
    if TeamRatings.objects.filter(rater_id=user_id, team_id=team_id, rated_id=teammate_id).exists():
        return redirect('viewTeam', team_id=team_id,)
    
    # Step 3: Handle GET and POST requests for the rating page
    if request.method == 'POST':
        # Extract multiple ratings from the form submission
        score_cooperation = request.POST.get('Cooperation')
        score_conceptual = request.POST.get('ConceptualContribution')
        score_practical = request.POST.get('PracticalContribution')
        score_workethic = request.POST.get('WorkEthic')
        comment = request.POST.get('message', '')

        # Validate each rating
        ratings = [score_cooperation, score_conceptual, score_practical, score_workethic]
        if not all(ratings) or any(int(rating) not in range(1, 6) for rating in ratings):
            return render(request, 'mainApp/assess.html', {
                'error': 'Invalid rating. Please provide a rating between 1 and 5 for all categories.',
                'session': request.session
            })

        # Step 4: Save all ratings in the database
        rating_record = TeamRatings(
            rater_id=user_id,
            team_id=team_id,
            rated_id=teammate_id,
            score_cooperation=score_cooperation,
            score_conceptual=score_conceptual,
            score_practical=score_practical,
            score_workethic=score_workethic,
            comment=comment
        )
        rating_record.save()
        
        return redirect('viewTeam', team_id=team_id)
    
    # If the request is GET, render the rating page
    teammate_name = MyUser.objects.get(id=teammate_id).name
    return render(request, 'student/assess.html', {'teammate_name': teammate_name, 'session': request.session})
    
def logout(request):
        del request.session['user_id']
        del request.session['name']
        # Logout message to be revisited for a later sprint: return render(request, 'mainApp/login.html', {'session': request.session, 'success': "Logout successsful"})
        return redirect('login')