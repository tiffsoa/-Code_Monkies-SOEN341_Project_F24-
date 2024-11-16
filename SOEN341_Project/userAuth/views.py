from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def loginView(request):
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
            
            return redirectAfterLogin(user)
        
        else:
            return render(request, 'userAuth/login.html', {'error': 'Account not found'})
    else:
        #If a user wasn't found, we send the user back to the login page
        #We should return an error message too!
        return render(request, 'userAuth/login.html', {'session':request.session, 'error':""})  # This returns to the user (request) the html file ( in mainApp/register.html) along with the data saved in our session dictionary ('session') which we can use in register.html

def redirectAfterLogin(user):
    #Redirect to the right home page depending on user (student or instructor)
    if user.instructor == True:
        return redirect('instructorHomePage') #Redirect to instructor home page
    else:
        return redirect('studentHomePage') #Redirect to student home page
    
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
            return render(request, 'userAuth/register.html', {'error': 'Passwords do not match.'})
        
        if MyUser.objects.filter(username=username).exists():
            return render(request, 'userAuth/register.html', {'error': 'Username already exists.'})
        
        if MyUser.objects.filter(email=email).exists():
            return render(request, 'userAuth/register.html', {'error': 'Email already exists.'})
        
        
        # Save user to the database
        user = MyUser(username=username, password=password, email=email, name=name, instructor=instructor)
        user.save()
        
        return redirect('login')  # Redirect to login page
    
    return render(request, 'userAuth/register.html', {'session': request.session})