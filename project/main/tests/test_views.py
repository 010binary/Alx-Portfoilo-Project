from django.test import TestCase, Client
from django.urls import reverse
from main.models import User, Competition, Candidate, Vote
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse

User = get_user_model()

class ViewTests(TestCase):

    def setUp(self):
        # Set up a test client and create a test user and a test competition
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            name='Test User',
            mobile_no='1234567890'
        )
        self.competition = Competition.objects.create(
            name="Test Competition",
            status="Active",
            start_date="2024-09-01",
            end_date="2024-09-30"
        )
        self.candidate = Candidate.objects.create(
            name="Test Candidate",
            competition=self.competition,
            total_votes=0
        )

    def test_register_view_get(self):
        # Test GET request to the register page
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_register_view_post_success(self):
        # Test POST request with valid data for registration
        response = self.client.post(reverse('register'), {
            'name': 'New User',
            'username': 'newuser',
            'mobile': '0987654321',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_register_view_post_invalid(self):
        # Test POST request with invalid data (password mismatch)
        response = self.client.post(reverse('register'), {
            'name': 'New User',
            'username': 'newuser',
            'mobile': '0987654321',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

    def test_login_view_post_success(self):
        # Test POST request with valid credentials for login
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_login_view_post_invalid(self):
        # Test POST request with invalid credentials for login
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_competition_view(self):
        # Test that the competition view works and returns the correct context
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('competition_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'competition.html')
        self.assertIn('trending_competitions', response.context)
        self.assertIn('other_competitions', response.context)

    def test_vote_view_success(self):
        # Test successful vote
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(reverse('cast_vote', args=[self.competition.id, self.candidate.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Successfully voted')
        self.candidate.refresh_from_db()
        self.assertEqual(self.candidate.total_votes, 1)

    def test_vote_view_already_voted(self):
        # Test voting again from the same user (should fail)
        Vote.objects.create(user=self.user, competition=self.competition, candidate=self.candidate, ip_address='127.0.0.1')
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(reverse('cast_vote', args=[self.competition.id, self.candidate.id]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'This device has already voted')

