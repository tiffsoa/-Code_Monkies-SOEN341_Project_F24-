from django.test import TestCase, Client
from django.urls import reverse
from userAuth.models import *  

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

        #Need a test group
        self.group = Projects.objects.create(
            project_name='Test Project',
            instructor_id=self.user.id  # Link project to instructor
        )

        # Link the student to the project
        Projects_to_Student_Relationships.objects.create(
            project_id=self.group.id,
            student_id=self.user2.id
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

    def test_successful_remove_student(self):
        response = self.client.post(reverse ('RemoveStudent', args=[self.user2.id,self.group.id]))
        self.assertEqual(response.status_code, 302)

    def test_successful_remove_group(self):
        response = self.client.post(reverse('deleteTeam', args={self.group.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_view_rating_page(self):
        response = self.client.post(reverse('instructorViewTeam', args={self.group.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_all_ratings(self):
        response = self.client.post(reverse('instructorOverallRatings'))
        self.assertEqual(response.status_code, 200)
    
    def test_team_rating_download(self):
        response = self.client.post(reverse('instructorTeamRatingsDownload', args={self.group.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_overallDownload(self):
        response = self.client.post(reverse('instructorOverallRatingsDownload'))
        self.assertEqual(response.status_code, 200)
