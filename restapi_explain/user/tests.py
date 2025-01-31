from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import AriyanspropertiesUser


class UserAPITestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user_data = {
            'user_name': 'Test User',
            'user_email': 'testuser@example.com',
            'user_password': '12345678',
            'user_type': 'admin',
            'phone_no': '1234567890'
        }
        self.client = APIClient()

    def test_register_user_success(self):
        """Test that a new user is successfully registered."""
        response = self.client.post('/api/register/', self.user_data, format='json')
        
        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if the response contains the expected data
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['user_name'], self.user_data['user_name'])
        self.assertEqual(response.data['user_email'], self.user_data['user_email'])

    def test_register_user_email_exists(self):
        """Test that registering with an existing email returns an error."""
        # Register the first user
        self.client.post('/api/register/', self.user_data, format='json')
        
        # Try to register a user with the same email
        response = self.client.post('/api/register/', self.user_data, format='json')
        
        # Check if the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Email already exists')

    def test_register_missing_fields(self):
        """Test that missing fields during registration return an error."""
        # Remove the 'phone_no' from user_data to simulate missing field
        incomplete_data = self.user_data.copy()
        incomplete_data.pop('phone_no')
        
        response = self.client.post('/api/register/', incomplete_data, format='json')
        
        # Check if the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'All fields are required.')
