from django.test import TestCase
from main.forms import RegisterForm, LoginForm, UpdateProfileForm

class FormTests(TestCase):
    
    def test_register_form_valid(self):
        form_data = {
            'name': 'John Doe',
            'username': 'johndoe',
            'mobile': '1234567890',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_password_mismatch(self):
        form_data = {
            'name': 'John Doe',
            'username': 'johndoe',
            'mobile': '1234567890',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match.', form.errors['__all__'])

    def test_login_form_valid(self):
        form_data = {
            'email': 'johndoe@example.com',
            'password': 'password123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_email(self):
        form_data = {
            'email': 'invalid-email',
            'password': 'password123'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'])

    def test_update_profile_form_valid(self):
        form_data = {
            'name': 'John Doe',
            'username': 'johndoe',
            'mobile_no': '1234567890',
            'email': 'johndoe@example.com',
            'address': '123 Main St'
        }
        form = UpdateProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_profile_form_missing_fields(self):
        form_data = {
            'name': 'John Doe',
            'username': 'johndoe',
            'mobile_no': '1234567890',
            'email': 'johndoe@example.com'
            # Missing address
        }
        form = UpdateProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['address'])
