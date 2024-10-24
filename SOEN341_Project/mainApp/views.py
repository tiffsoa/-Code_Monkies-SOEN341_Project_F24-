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
            'is_open': instructor_project.open, 
        }
        projects_info.append(project_data)
    
    #Now, we have a list with dictionaries sent to the frontend. It looks something like this:
    # [{project_id:123123,project_name:"Some name",is_open:1},{project_id:9345353,project_name:"Some other name",is_open:0}]
    # Step 4: Render the information to the template
    return render(request, 'mainApp/homepageinstructor.html', {'projects': projects_info})

def CloseOpenTeam(request, team_id):
    #placeholder
    return redirect('instructorHomePage')

def teamRatingsInstructor(request, team_id):
    #placeholder
    return redirect('instructorHomePage')



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
            'is_open': Projects.objects.get(id=projectID).open, 
            'instructor_name': MyUser.objects.get(id=instructorID).name
        }
        projects_info.append(project_data)
    
    
    # Now, we have a list with dictionaries sent to the frontend. It looks something like this:
    # [{project_id:123123,project_name:"Some name",is_open:1, instructor_name: "John"}, {project_id:9345353,project_name:"Some other name",is_open:0, instructor_name: "Jane"}]
    # Step 4: Render the information to the template
    return render(request, 'mainApp/homepagestudent.html', {'projects': projects_info})

def viewTeam(request, team_id):
    user_id = request.session.get('user_id')  # get logged-in user's ID from session

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
    context = {'students': student_list}

    return render(request, 'students_in_team.html', context) ### NEED TO MODIFY STUDENTS_IN_TEAM DEPENDING ON THE NAME THE FRONTEND GIVES THE PAGE

def teamRatingsStudent(request, team_id):
    #placeholder
    return redirect('studentHomePage')

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
    if request.method == "POST": 
        del request.session['user_id']
        del request.session['name']
        # Logout message to be revisited for sprint 2: return render(request, 'mainApp/login.html', {'session': request.session, 'success': "Logout successsful"})
        return redirect('login')


