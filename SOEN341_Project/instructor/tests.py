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


