from django.test import TestCase, Client
from django.urls import reverse
from mainApp.models import *  # Adjust if you have a custom user model

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

#Test for creating group
class createGroupTest(TestCase):
    def setUp(self):
        #Need the instructor made
        self.user = MyUser.objects.create(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            name='Test User',
            instructor=1
        )

        #Need a test student
        self.user2 = MyUser.objects.create(
            username='testuser2',
            password='testpassword',
            email='testuser2@example.com',
            name='Test User2',
            instructor=0
        )

        self.client=Client() #Need the fake server

        # Set session variables
        session = self.client.session
        session['user_id'] = self.user.id  # Add user ID to session
        session.save()  # Save the session to persist the changes

    def test_successful_create_group(self):
        response=self.client.post(reverse('createGroup'),{
            "project_name":"the best",
            "user_name[]":"testuser2"
        })
        
        # Check if the user is redirected 
        self.assertEqual(response.status_code, 302)

class submitRatingTest(TestCase):
    def setUp(self):
        # Create a test instructor
        self.instructor = MyUser.objects.create(
            username='test_instructor',
            password='password_instructor',  # Normally, you'd use hashed passwords
            email='instructor@example.com',
            name='Instructor Name',
            instructor=True  # Set to True to mark as instructor
        )

        # Create a test student
        self.student = MyUser.objects.create(
            username='test_student',
            password='password_student',
            email='student@example.com',
            name='Student Name',
            instructor=False  # False for students
        )

        # Create a test group (project)
        self.group = Projects.objects.create(
            project_name='Test Project',
            instructor_id=self.instructor.id  # Link project to instructor
        )

        # Link the student to the project
        Projects_to_Student_Relationships.objects.create(
            project_id=self.group.id,
            student_id=self.student.id
        )

        # Initialize the test client
        self.client = Client()

        #set session data for  student
        session = self.client.session
        session['user_id'] = self.student.id  # Example: log in as instructor
        session.save()

    def test_submit_rating_successful(self):
        response=self.client.post(reverse('createGroup',args=[self.group.id,self.group.id]),{
            "Cooperation":"5",
            "ConceptualContribution":"3",
            "PracticalContribution":"2",
            "WorkEthic":"5"
        })
        
        # Check if the user is redirected 
        self.assertEqual(response.status_code, 302)
    



