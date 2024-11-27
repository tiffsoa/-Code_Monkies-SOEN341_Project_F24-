from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from userAuth.models import *
import csv

#this is the main file we will work on
#here, we will create different views or routes that we can access on our website

#This page has all the functions whose job is to return an HTML page when executed.
#Note that all variables which we want to keep attributed to a certain user is saved in the dictionary "session" https://reintech.io/blog/working-with-sessions-in-django-tutorial


def instructorHomeView(request):
    # Step 1: Retrieve the user ID from session
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Handle case where user_id is not in session (e.g., user is not logged in)
        return redirect('login')  # Redirect to login page 
    
    # Step 2: Query the projects table for the instructor’s projects
    instructor_projects = Projects.objects.filter(instructor_id=user_id)
    
    # Step 3: For each project, get project info 
    projects_info = []
    for instructor_project in instructor_projects:
        projectID = instructor_project.id  
	
        
        # Get the project details
        project_data = {
            'project_id': projectID,
            'project_name': instructor_project.project_name,
        }
        projects_info.append(project_data)
    
    #Now, we have a list with dictionaries sent to the frontend. It looks something like this:
    # [{project_id:123123,project_name:"Some name",is_open:1},{project_id:9345353,project_name:"Some other name",is_open:0}]
    # Step 4: Render the information to the template
    return render(request, 'instructor/homepageinstructor.html', {'projects': projects_info})


def ratingLogicOverall(request):
    #get all projects assigned to given instructor
    user_id = request.session.get('user_id')
    instructor_projects = Projects.objects.filter(instructor_id=user_id)

    rating_info = [] #Create list of students' ratings
    #iterate thru all project ids of given instructor
    for project_id in instructor_projects:
        currentID = project_id.id #Obtain current project id

        #get all users of the current project
        users = Projects_to_Student_Relationships.objects.filter(project_id = currentID)
        #iterate thru all users of the current project
        for user in users:
            currentUserID = user.student_id #Obtain current user ID

            ratings = TeamRatings.objects.filter(team_id=currentID, rated_id=currentUserID) #Obtain a list of all ratings of a given student

            teammate_ids = Projects_to_Student_Relationships.objects.filter(project_id=currentID).values_list('student_id', flat=True).distinct() #Obtain a list of all teammates of a given student

            userCounter = 0 #Number of users who rated a given student

            cooperation = 0 #Cooperation score
            conceptual = 0 #Conception score
            practical = 0 #Practical score
            workethic = 0 #Work ethic score

            for teammate_id in teammate_ids: 
                if teammate_id==currentUserID: #continue looping thru all teammates if it's the current student
                    continue

                rating = ratings.filter(rater_id = teammate_id).first() #Obtain the rating of current teammate

                cooperation += rating.score_cooperation if rating else 0 #add all ratings together
                conceptual += rating.score_conceptual if rating else 0
                practical += rating.score_practical if rating else 0
                workethic += rating.score_workethic if rating else 0

                if rating: #increment a user that rated by 1 if they have made a rating
                    userCounter += 1

            if userCounter != 0: #If current student has been rated, make an average of all individual scores
                cooperation = round(cooperation/userCounter, 2)
                conceptual = round(conceptual/userCounter, 2)
                practical = round(practical/userCounter, 2)
                workethic = round(workethic/userCounter, 2)
            

            average = round((cooperation + conceptual + practical + workethic)/4, 2) #Calculate overall average

            if (conceptual or cooperation or practical or workethic) == 0:
                conceptual = "-"
                cooperation = "-"
                practical = "-"
                workethic = "-"
                average = "-"

            rating_data = { #Create rating data structure
                'id': currentUserID,
                'username': MyUser.objects.get(id = currentUserID).username,
                'name': MyUser.objects.get(id = currentUserID).name,
                'team': Projects.objects.get(id = currentID).project_name,
                'cooperation': cooperation,
                'conceptual': conceptual,
                'practical': practical,
                'work_ethic': workethic,
                'average': average,
                'numOfRespondents': userCounter
            }

            rating_info.append(rating_data) #add rating of student to list
    return rating_info

def instructorOverallRatings(request): #simply returns a render of the html file with the rating calculated
    return render(request, 'instructor/instructorOverallRatings.html', {'ratings': ratingLogicOverall(request)})

def instructorOverallRatingsDownload(request):
    if request.method == 'GET':
        response = HttpResponse(content_type="text/csv") #Create response to download csv file
        response['Content-Disposition'] = 'attachment; filename="userRatings.csv' #assign filename

        writer = csv.writer(response)
        ratings = ratingLogicOverall(request) #List of dicts of all overall ratings
        for rating in ratings: #Loop through each element of ratings list and write each content of dict to row
            writer.writerow([rating.get('id'), rating.get('username'), rating.get('name'), rating.get('team'), rating.get('cooperation'),rating.get('conceptual'), rating.get('practical'), rating.get('work_ethic'), rating.get('average'), rating.get('numOfRespondents')])
        return response #trigger download
    return render(request, 'instructor/instructorOverallRatings.html', {'ratings': ratingLogicOverall(request)})

def instructorViewTeam(request, team_id):
    user_id = request.session.get('user_id')  # get logged-in user's ID from session
    error=""
    success=""
    if request.method == 'POST':
        # Extract data from the HTML form
        username = request.POST.get('username')

        #Search for a match in our database
        if MyUser.objects.filter(username=username, instructor=0).exists():
            #if match found
            new_user_id=MyUser.objects.get(username=username).id
            # check if student already in taem
            if Projects_to_Student_Relationships.objects.filter(project_id=team_id, student_id=new_user_id).exists():
                error=f"Student {request.POST.get('username')} is already in this team."
            else:
                Projects_to_Student_Relationships.objects.create(project_id=team_id, student_id=new_user_id)
                success="New user added successfully!"
        else:   
            error=f"Student {request.POST.get('username')} does not exist."

    teamName = Projects.objects.get(id = team_id).project_name # get team name

    # Find all students un the team (project) with the given team number
    team_memberships = Projects_to_Student_Relationships.objects.filter(project_id=team_id)

    # Extract the student details for each membership
    student_list = []
    for membership in team_memberships:
        student = MyUser.objects.get(id=membership.student_id)
        student_list.append({student.name: student.id})

    # Pass the student list to the front-end (in a list of maps)
    context = {'students': student_list, 'teamName': teamName, 'teamID': team_id,"error":error, "success":success}
    #i.e. context looks something like {'students':["name1":id1,"name2":id2,"name3",id3]}
    return render(request, 'instructor/instructorEditTeam.html', context) ### NEED TO MODIFY STUDENTS_IN_TEAM DEPENDING ON THE NAME THE FRONTEND GIVES THE PAGE

def createGroupPage(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES: # Passing on to groupCreationCSV causes errors so i copypasted the function here for now
            csv_file = request.FILES.get("csv_file")
            if not csv_file.name.endswith('.csv'): #if not a .csv file
                return render(request, 'instructor/createGroup.html', {'error': 'File is not a .csv'})
            if csv_file.multiple_chunks(): #if the file is too large
                return render(request, 'instructor/createGroup.html', {'error': 'File is too large'})

            file_data = csv_file.read().decode("utf-8")	#read the file	

            lines = file_data.split("\n")

            for line in lines:	#loop over the lines and save them in db.
                line = line.strip()  # Remove any leading/trailing whitespace
                if not line:  # Skip empty lines
                    continue		
                fields = line.split(",")
                groupName = fields[0]
                if Projects.objects.filter(project_name = groupName).exists() == True: #If group name already exists (proper error handling at a later sprint)
                        continue
                idList = []
                for user in fields[1:]: #generally the same process as normal group creation
                    if MyUser.objects.filter(username=user, instructor = 0).exists(): #check if the student users on the list exist in the database
                        userExists = MyUser.objects.get(username=user)
                        id = userExists.id
                        idList.append(id)
                    else:
                        return render(request, 'instructor/createGroup.html', {'error': groupName + 'has not been added because user' + user + 'does not exist.'}) #Error message if user doesn't exist
                newProject = Projects(project_name = groupName, instructor_id  = request.session.get('user_id'))
                newProject.save() #Saving project to database

                projectID = newProject.id #Retrieve new project id

                for id in idList: #iterate through all ids and create their relationship with their respective projects
                        projectStudent = Projects_to_Student_Relationships(project_id = projectID, student_id = id)
                        projectStudent.save()
                return redirect('instructorHomePage')
            return render(request, 'instructor/createGroup.html', {'session': request.session})
        
        projectName = request.POST.get('project_name')
        userList = request.POST.getlist('user_name[]')
        idList = []
        if Projects.objects.filter(project_name = projectName).exists() == False:
            for user in userList:
                if MyUser.objects.filter(username=user, instructor = 0).exists(): #check if the student users on the list exist in the database
                    userExists = MyUser.objects.get(username=user)
                    id = userExists.id
                    idList.append(id) #if they exist, add their student id to the id list
                elif MyUser.objects.filter(username=user, instructor = 1).exists():
                    return render(request, 'instructor/createGroup.html', {'error': user + ' is an instructor.'}) #Error message if user is an instructor
                else:
                    return render(request, 'instructor/createGroup.html', {'error': user + ' does not exist.'}) #Error message if user doesn't exist
            newProject = Projects(project_name = projectName, instructor_id  = request.session.get('user_id'))
            newProject.save() #Saving project to database

            projectID = newProject.id #Retrieve new project id

            for id in idList: #iterate through all ids and create their relationship with their respective projects
                projectStudent = Projects_to_Student_Relationships(project_id = projectID, student_id = id)
                projectStudent.save()
            
            return redirect('instructorHomePage')
        else:
            return render(request, 'instructor/createGroup.html', {'error': projectName + ' already exists.'})
    
    return render(request, 'instructor/createGroup.html', {'session': request.session})

def createGroupCSV(request): # IGNORE THIS FOR NOW
    if request.method == 'POST':
        
        csv_file = request.POST.get("csv_file")
        if not csv_file.name.endswith('.csv'): #if not a .csv file
            return render(request, 'mainApp/createGroup.html', {'error': 'File is not a .csv'})
        if csv_file.multiple_chunks(): #if the file is too large
            return render(request, 'mainApp/createGroup.html', {'error': 'File is too large'})

        file_data = csv_file.read().decode("utf-8")	#read the file	

        lines = file_data.split("\n")

        for line in lines:	#loop over the lines and save them in db.
            line = line.strip()  # Remove any leading/trailing whitespace
            if not line:  # Skip empty lines
                continue		
            fields = line.split(",")
            groupName = fields[0]
            idList = []
            for user in fields[1:]: #generally the same process as normal group creation
                if MyUser.objects.filter(username=user, instructor = 0).exists(): #check if the student users on the list exist in the database
                    userExists = MyUser.objects.get(username=user)
                    id = userExists.id
                    idList.append(id)
                else:
                    return render(request, 'mainApp/createGroup.html', {'error': groupName + 'has not been added because user' + user + 'does not exist.'}) #Error message if user doesn't exist
            newProject = Projects(project_name = groupName, instructor_id  = request.session.get('user_id'))
            newProject.save() #Saving project to database

            projectID = newProject.id #Retrieve new project id

            for id in idList: #iterate through all ids and create their relationship with their respective projects
                    projectStudent = Projects_to_Student_Relationships(project_id = projectID, student_id = id)
                    projectStudent.save()
        return redirect('instructorHomePage')
    
    return render(request, 'mainApp/createGroup.html', {'session': request.session})
        
def logout(request):
        del request.session['user_id']
        del request.session['name']
        # Logout message to be revisited for a later sprint: return render(request, 'mainApp/login.html', {'session': request.session, 'success': "Logout successsful"})
        return redirect('login')


def RemoveStudent(request,team_id,teammate_id):
    #delete student from team
    Projects_to_Student_Relationships.objects.filter(
        student_id=teammate_id, 
        project_id=team_id
    ).delete()

    #delete students ratings
    TeamRatings.objects.filter(team_id=team_id).filter(rater_id=teammate_id).delete()
    TeamRatings.objects.filter(team_id=team_id).filter(rated_id=teammate_id).delete()

    #if no more students, delete group
    if not Projects_to_Student_Relationships.objects.filter(project_id=team_id).exists():
        Projects.objects.filter(id=team_id).delete()
        return redirect("instructorHomePage")


    return redirect("instructorViewTeam", team_id=team_id)

def deleteTeam(request, team_id ):
    #Delete all students from team
    Projects_to_Student_Relationships.objects.filter(project_id=team_id).delete()

    #Delete all ratings from team
    TeamRatings.objects.filter(team_id=team_id).delete()

    #Delete the team
    Projects.objects.filter(id=team_id).delete()

    return redirect("instructorHomePage")
    
def instructorTeamRatings(request, team_id):
    # Retrieve ratings for each member of the team
    teammate_ids = Projects_to_Student_Relationships.objects.filter(project_id=team_id).values_list('student_id', flat=True).distinct()
    ratings_list = []

    for teammate_id in teammate_ids:
        teammate = MyUser.objects.get(id=teammate_id)
        
        # Get the ratings given by others for the current teammate in the team
        ratings = TeamRatings.objects.filter(team_id=team_id, rated_id=teammate_id)

        # Initialize rating data
        rating_data = {
            "name": teammate.name,
            "cooperation": None,
            "conceptual": None,
            "practical": None,
            "work_ethic": None,
            "average_across_all": None
        }

        # If the teammate has ratings, calculate averages
        if ratings:
            score_cooperation = sum([rating.score_cooperation for rating in ratings]) / len(ratings)
            score_conceptual = sum([rating.score_conceptual for rating in ratings]) / len(ratings)
            score_practical = sum([rating.score_practical for rating in ratings]) / len(ratings)
            score_workethic = sum([rating.score_workethic for rating in ratings]) / len(ratings)
            average_across_all = (score_cooperation + score_conceptual + score_practical + score_workethic) / 4

            rating_data.update({
                "cooperation": round(score_cooperation, 2),
                "conceptual": round(score_conceptual, 2),
                "practical": round(score_practical, 2),
                "work_ethic": round(score_workethic, 2),
                "average_across_all": round(average_across_all, 2)
            })
        
        ratings_list.append(rating_data)

    # Pass the data to the template
    return render(request, 'instructor/instructorTeamRatings.html', {'ratings': ratings_list,"team_id":team_id})

def instructorTeamRatingsDownload(request, team_id):
    # Prepare the HTTP response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="team_{team_id}_ratings.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Cooperation', 'Conceptual', 'Practical', 'Work Ethic', 'Average Across All'])

    # Retrieve and write ratings data for each teammate
    teammate_ids = Projects_to_Student_Relationships.objects.filter(project_id=team_id).values_list('student_id', flat=True).distinct()

    for teammate_id in teammate_ids:
        teammate = MyUser.objects.get(id=teammate_id)
        ratings = TeamRatings.objects.filter(team_id=team_id, rated_id=teammate_id)

        if ratings:
            score_cooperation = sum([rating.score_cooperation for rating in ratings]) / len(ratings)
            score_conceptual = sum([rating.score_conceptual for rating in ratings]) / len(ratings)
            score_practical = sum([rating.score_practical for rating in ratings]) / len(ratings)
            score_workethic = sum([rating.score_workethic for rating in ratings]) / len(ratings)
            average_across_all = (score_cooperation + score_conceptual + score_practical + score_workethic) / 4

            writer.writerow([
                teammate.name,
                round(score_cooperation, 2),
                round(score_conceptual, 2),
                round(score_practical, 2),
                round(score_workethic, 2),
                round(average_across_all, 2)
            ])
        else:
            writer.writerow([teammate.name, "", "", "", "", ""])

    return response

def instructorSettings(request):
    #insert logic
    return render(request, 'instructor/instructorSettings.html', {'session': request.session})
