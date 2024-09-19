from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import MyUser

#This page has all the functions whose job is to return an HTML page when executed.
#Note that all variables which we want to keep attributed to a certain user is saved in the dictionary "session" https://reintech.io/blog/working-with-sessions-in-django-tutorial

def register(request):
    if request.method == 'POST':
        # Extract data from the HTML form
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate data
        if password != confirm_password:
            return HttpResponse("Passwords do not match.") #Instead of doing this, we should return this message as part of context!
        #This line below checks each row of the MyUser table for a matching username
        if MyUser.objects.filter(username=username).exists():
            return HttpResponse("Username already exists.") #Return this message with page

        # Create user. This adds a new row to our database
        User(username=username,password=password).save()
        #To see all possible table methods, https://docs.djangoproject.com/en/5.1/topics/db/queries/
        return redirect('login')  # Redirect to login page after registration. Should add a success message too!
    else:
        #If the the request's method wasn't post (i.e. the user wasn't filling in a form) just generate the page
        return render(request, 'mainApp/register.html', {'session':request.session}) # This returns to the user (request) the html file (mainApp/register.html) along with the data saved ('session') which we can use in register.html


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
            request.session['username']= user.username
            if user.type=="instructor":
                return redirect('instructorHomePage')
            return redirect('home') # and now we redirect to our 'home' view
        else:
            return render(request, 'mainApp/login.html', {'error': 'Username and password dont match'})
    else:
        #If a user wasn't found, we send the user back to the login page
        #We should return an error message too!
        return render(request, 'mainApp/login.html', {'session':request.session})  # This returns to the user (request) the html file ( in mainApp/register.html) along with the data saved in our session dictionary ('session') which we can use in register.html

def home_view(request):
    #Should add code such that only logged in users (those who we added a user_id in their session dictionary) can view this page
    return render(request,'mainApp/home.html',{})
