from django.test import TestCase, Client
from django.urls import reverse
from userAuth.models import *  

#This tests login and accessing home pages
class LoginViewTest(TestCase):
    #How testing works: every method starting with test_ is ran individually, and for each the setUp is ran first which adds the test entry to the test database.

    def setUp(self): #The setup method is what's ran everytime
        # Create a user for testing
        #MyUser.objects.create creates the user, but it returns the object to it in case we need it, so we save it in user variable
        self.user = MyUser.objects.create(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            name='Test User',
            instructor=1
        )
        self.user2 = MyUser.objects.create(
            username='testuser2',
            password='testpassword',
            email='testuser2@example.com',
            name='Test User2',
            instructor=0
        )
        #This makes a client object which allows us to simulate GET and POSTs to the URL
        self.client = Client()

    def test_successful_login_instructor(self):
        # Simulate a login with correct credentials

        #What this does is, using our client object, it posts the data to the URL we put, which then redirects to the login function.
        #Doing self.client.post sends the message, and will return the response. 
        #Response contains: the HTTP status code, the rendered template (if applicable), context data, and content.
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        

        # Check if the user is redirected (assuming `redirect_after_login` redirects to another page)
        #assertEqual tests for equality and gives false and fails test if not equal
        self.assertEqual(response.status_code, 302)
        
        # Verify session data
        session = self.client.session
        self.assertEqual(session['user_id'], self.user.id)
        self.assertEqual(session['name'], self.user.name)

    def test_successful_login_student(self):
       
        response = self.client.post(reverse('login'), {
            'username': 'testuser2',
            'password': 'testpassword'
        })
        

        # Check if the user is redirected (assuming `redirect_after_login` redirects to another page)
        #assertEqual tests for equality and gives false and fails test if not equal
        self.assertEqual(response.status_code, 302)
        
#This tests registration
class registerViewTest(TestCase):
    def setUp(self):
        self.client=Client() #Just need the fake server for this one

    def test_succesful_register(self):
        response=self.client.post(reverse('register'),{
            'username': 'testuser',
            'password': 'testpassword',
            'email':'testuser@example.com',
            'name':'Test User',
            'role':"teacher",
        })
        
        # Check if the user is redirected 
        self.assertEqual(response.status_code, 200)

