from django.test import TestCase
from django.utils import timezone
from main.models import User, Competition, Candidate, Vote

class UserModelTest(TestCase):
    
    def setUp(self):
        """Set up some basic data to use in tests."""
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            name="Test User",
            mobile_no="1234567890",
            password="password123"
        )
    
    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.mobile_no, "1234567890")
        self.assertTrue(self.user.check_password("password123"))
    
    def test_string_representation(self):
        """Test the string representation of the User model."""
        self.assertEqual(str(self.user), "testuser")
    
    def test_email_is_lowercase(self):
        """Test that the email is saved in lowercase."""
        user = User.objects.create_user(
            email="USER@EXAMPLE.COM",
            username="testuser2",
            name="Test User 2",
            mobile_no="0987654321",
            password="password123"
        )
        self.assertEqual(user.email, "user@example.com")

class CompetitionModelTest(TestCase):

    def setUp(self):
        """Set up a competition to use in the test."""
        self.competition = Competition.objects.create(
            name="Test Competition",
            description="A test competition",
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=7),
            status="Active"
        )
    
    def test_competition_creation(self):
        """Test that a competition is created successfully."""
        self.assertEqual(self.competition.name, "Test Competition")
        self.assertEqual(self.competition.status, "Active")
    
    def test_string_representation(self):
        """Test the string representation of the Competition model."""
        self.assertEqual(str(self.competition), "Test Competition")

class CandidateModelTest(TestCase):

    def setUp(self):
        """Set up a candidate and competition for the test."""
        self.competition = Competition.objects.create(
            name="Test Competition",
            description="A test competition",
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=7),
            status="Active"
        )
        self.candidate = Candidate.objects.create(
            name="Test Candidate",
            description="A test candidate",
            competition=self.competition,
            total_votes=10
        )
    
    def test_candidate_creation(self):
        """Test that a candidate is created successfully."""
        self.assertEqual(self.candidate.name, "Test Candidate")
        self.assertEqual(self.candidate.total_votes, 10)
        self.assertEqual(self.candidate.competition.name, "Test Competition")

class VoteModelTest(TestCase):

    def setUp(self):
        """Set up a user, competition, candidate, and vote for the test."""
        self.user = User.objects.create_user(
            email="voter@example.com",
            username="voter",
            name="Voter User",
            mobile_no="1234567890",
            password="password123"
        )
        self.competition = Competition.objects.create(
            name="Test Competition",
            description="A test competition",
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=7),
            status="Active"
        )
        self.candidate = Candidate.objects.create(
            name="Test Candidate",
            description="A test candidate",
            competition=self.competition,
            total_votes=10
        )
        self.vote = Vote.objects.create(
            user=self.user,
            competition=self.competition,
            candidate=self.candidate,
            ip_address="127.0.0.1"
        )

    def test_vote_creation(self):
        """Test that a vote is created successfully."""
        self.assertEqual(self.vote.user.username, "voter")
        self.assertEqual(self.vote.competition.name, "Test Competition")
        self.assertEqual(self.vote.candidate.name, "Test Candidate")
        self.assertEqual(self.vote.ip_address, "127.0.0.1")
    
    def test_string_representation(self):
        """Test the string representation of the Vote model."""
        self.assertEqual(
            str(self.vote),
            "Vote by voter for Test Candidate in Test Competition"
        )
