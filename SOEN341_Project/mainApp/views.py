from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

#this is the main file we will work on
#here, we will create different views or routes that we can access on our website

#This page has all the functions whose job is to return an HTML page when executed.
#Note that all variables which we want to keep attributed to a certain user is saved in the dictionary "session" https://reintech.io/blog/working-with-sessions-in-django-tutorial



def login_view(request):
    if request.method == 'POST':
        # Extract data from the HTML form
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Search for a match in our database
        #To see all possible table methods, https://docs.djangoproject.com/en/5.1/topics/db/queries/
        if MyUser.objects.filter(username=username, password=password).exists():
            #if match found
            user = MyUser.objects.get(username=username) #If a match exists, we store the object of that match in user
            request.session['user_id'] = user.id # And then we want to save the logged in user's id, so we store it in our 'session' dictionary (each user has a unique one)
            request.session['name']= user.name
            
            return redirect_after_login(user)
        
        else:
            return render(request, 'mainApp/login.html', {'error': 'Account not found'})
    else:
        #If a user wasn't found, we send the user back to the login page
        #We should return an error message too!
        return render(request, 'mainApp/login.html', {'session':request.session, 'error':""})  # This returns to the user (request) the html file ( in mainApp/register.html) along with the data saved in our session dictionary ('session') which we can use in register.html

def redirect_after_login(user):
    #Redirect to the right home page depending on user (student or instructor)
    if user.instructor == True:
        return redirect('instructorHomePage') #Redirect to instructor home page
    else:
        return redirect('studentHomePage') #Redirect to student home page

def instructor_home_view(request):
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
    return render(request, 'mainApp/homepageinstructor.html', {'projects': projects_info})

def CloseOpenTeam(request, team_id):
    #placeholder
    return redirect('instructorHomePage')

def instructorTeamRatings(request, team_id):
    #placeholder
    return render(request, 'mainApp/instructorTeamRatings.html')

def instructorTeamRatingsDownload(request, team_id):
    #placeholder
    return render(request, 'mainApp/instructorTeamRatings.html')

def instructorOverallRatings(request):
    #placeholder
    return render(request, 'mainApp/instructorOverallRatings.html')

def instructorOverallRatingsDownload(request):
    #placeholder
    return render(request, 'mainApp/instructorOverallRatings.html')

def student_home_view(request):
    # Step 1: Retrieve the user ID from session
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Handle case where user_id is not in session (e.g., user is not logged in)
        return redirect('login')  # Redirect to login page
    
    # Step 2: Query the Projects_to_Student_Relationships table for the projects the user is in
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
    return render(request, 'mainApp/homepagestudent.html', {'projects': projects_info})

def viewTeam(request, team_id):
    user_id = request.session.get('user_id')  # get logged-in user's ID from session

    teamName = Projects.objects.get(id = team_id).project_name # get team name

    # Find all students un the team (project) with the given team number
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
    return render(request, 'mainApp/students_in_team.html', context) ### NEED TO MODIFY STUDENTS_IN_TEAM DEPENDING ON THE NAME THE FRONTEND GIVES THE PAGE

def instructorViewTeam(request, team_id):
    user_id = request.session.get('user_id')  # get logged-in user's ID from session

    teamName = Projects.objects.get(id = team_id).project_name # get team name

    # Find all students un the team (project) with the given team number
    team_memberships = Projects_to_Student_Relationships.objects.filter(project_id=team_id)

    # Extract the student details for each membership
    student_list = []
    for membership in team_memberships:
        student = MyUser.objects.get(id=membership.student_id)
        student_list.append({student.name: student.id})

    # Pass the student list to the front-end (in a list of maps)
    context = {'students': student_list, 'teamName': teamName, 'teamID': team_id}
    #i.e. context looks something like {'students':["name1":id1,"name2":id2,"name3",id3]}
    return render(request, 'mainApp/instructors_students_in_team.html', context) ### NEED TO MODIFY STUDENTS_IN_TEAM DEPENDING ON THE NAME THE FRONTEND GIVES THE PAGE

def studentTeamRatings(request, team_id):
    return render(request, 'mainApp/studentTeamRatings.html')

def studentTeamRatingsDownload(request, team_id):
    #placeholder
    return render(request,"mainApp/studentTeamRatings.html")

def createGroupPage(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES: # Passing on to groupCreationCSV causes errors so i copypasted the function here for now
            csv_file = request.FILES.get("csv_file")
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
                if Projects.objects.filter(project_name = groupName).exists() == True: #If group name already exists (proper error handling at a later sprint)
                        continue
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
                    return render(request, 'mainApp/createGroup.html', {'error': user + ' is an instructor.'}) #Error message if user is an instructor
                else:
                    return render(request, 'mainApp/createGroup.html', {'error': user + ' does not exist.'}) #Error message if user doesn't exist
            newProject = Projects(project_name = projectName, instructor_id  = request.session.get('user_id'))
            newProject.save() #Saving project to database

            projectID = newProject.id #Retrieve new project id

            for id in idList: #iterate through all ids and create their relationship with their respective projects
                projectStudent = Projects_to_Student_Relationships(project_id = projectID, student_id = id)
                projectStudent.save()
            
            return redirect('instructorHomePage')
        else:
            return render(request, 'mainApp/createGroup.html', {'error': projectName + ' already exists.'})
    
    return render(request, 'mainApp/createGroup.html', {'session': request.session})

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
        

def register(request): #register main method to function "Backend"
    if request.method == 'POST':
        # Extract data from the HTML form
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        name = request.POST.get('name')

        if request.POST['role'] == "teacher": # Was unable to make it work with request.POST.get
            instructor = 1
        else:
            instructor = 0

        # Validate data
        if password != confirm_password:
            return render(request, 'mainApp/register.html', {'error': 'Passwords do not match.'})
        
        if MyUser.objects.filter(username=username).exists():
            return render(request, 'mainApp/register.html', {'error': 'Username already exists.'})
        
        if MyUser.objects.filter(email=email).exists():
            return render(request, 'mainApp/register.html', {'error': 'Email already exists.'})
        
        
        # Save user to the database
        user = MyUser(username=username, password=password, email=email, name=name, instructor=instructor)
        user.save()
        
        return redirect('login')  # Redirect to login page
    
    return render(request, 'mainApp/register.html', {'session': request.session})

def logout(request):
        del request.session['user_id']
        del request.session['name']
        # Logout message to be revisited for a later sprint: return render(request, 'mainApp/login.html', {'session': request.session, 'success': "Logout successsful"})
        return redirect('login')


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
    return render(request, 'mainApp/assess.html', {'teammate_name': teammate_name, 'session': request.session})


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


