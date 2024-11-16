from django.test import TestCase, Client
from django.urls import reverse
from userAuth.models import *  # Adjust if you have a custom user model

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
        response=self.client.post(reverse('RateTeammate',args=[self.group.id,self.group.id]),{
            "Cooperation":"5",
            "ConceptualContribution":"3",
            "PracticalContribution":"2",
            "WorkEthic":"5"
        })
        
        # Check if the user is redirected 
        self.assertEqual(response.status_code, 302)
    