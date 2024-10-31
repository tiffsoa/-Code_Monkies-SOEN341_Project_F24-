from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User  # Adjust if you have a custom user model

class UserRegistrationTest(TestCase):
    def test_student_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'studentuser',
            'password': 'password123',
            'email': 'studentuser@example.com',
            'role': 'student'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect on success

    def test_teacher_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'teacheruser',
            'password': 'password123',
            'email': 'teacheruser@example.com',
            'role': 'teacher'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect on success

    def test_registration_with_existing_username(self):
        User.objects.create_user(username='existinguser', password='password123', email='existinguser@example.com')
        response = self.client.post(reverse('register'), {
            'username': 'existinguser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'role': 'student'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Username already exists', response.content.decode())


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Account not found', response.content.decode())


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='password123', email='profileuser@example.com')
        self.client.login(username='profileuser', password='password123')

    def test_update_profile(self):
        response = self.client.post(reverse('update_profile'), {
            'bio': 'New bio content'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Profile updated successfully', response.content.decode())
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'New bio content')







