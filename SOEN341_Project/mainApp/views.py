from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import MyUser

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
    #fect the necessary info when we will have a database
    return render(request,'mainApp/homepageinstructor.html',{})

def student_home_view(request):
    #Fetch necessary data for the student home page
    #for the first srpint, we do not have a database yet
    return render(request,'mainApp/homepagestudent.html',{})


def register(request):
    if request.method == 'POST':
        # Extract data from the HTML form
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        instructor = request.POST.get('instructor') == 'on'  # assuming checkbox for instructor
        
        # Validate data
        if password != confirm_password:
            return render(request, 'mainApp/register.html', {'error': 'Passwords do not match.'})
        
        if MyUser.objects.filter(username=username).exists():
            return render(request, 'mainApp/register.html', {'error': 'Username already exists.'})
        
        if MyUser.objects.filter(email=email).exists():
            return render(request, 'mainApp/register.html', {'error': 'Email already exists.'})
        
        # Save user to the database
        user = MyUser(username=username, password=password, email=email, name=name, is_instructor=instructor)
        user.save()
        
        return redirect('login')  # Redirect to login page
    
    return render(request, 'mainApp/register.html', {'session': request.session})

