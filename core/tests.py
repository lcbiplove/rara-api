import json
import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.utils import jwt_encode_payload, jwt_get_payload

# def sample_user(email='test@gmail.com', password="testpass"):
#     """Create a simple user"""
#     return get_user_model().objects.create_user(email, password)

LOGIN_URL = reverse('login')

PROFILE_URL = reverse('profile')

JWKS_URL = reverse('certs')

class LoginTest(TestCase):
    """Login related test"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='biplove@gmail.com', 
            password='mystrongPassword', 
            name='Biplove Lamichhane', 
            location='Tanahun',
        )

    def test_invalid_login(self):
        """Test that login is required to access the endpoint"""
        payload = {
            'email': 'biplove@gmail.com',  
            'password': '1234',
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_login(self):
        """Test for successful login"""
        payload = {
            'email': 'biplove@gmail.com', 
            'password': 'mystrongPassword',
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in res.data)


class PrivateProfileTest(TestCase):
    """Test related ot accessing private user data"""

    def setUp(self):
        self.client = APIClient()
        self.user_dict = {
            'email': 'biplove@gmail.com', 
            'password': 'mystrongPassword', 
            'name': 'Biplove Lamichhane', 
            'location': 'Tanahun',
        }
        self.user = get_user_model().objects.create_user(**self.user_dict)

    def get_token(self):
        payload = {
            'email': 'biplove@gmail.com', 
            'password': 'mystrongPassword',
        }
        res = self.client.post(LOGIN_URL, payload)
        token = res.data['token']
        return token

    def test_for_not_logged_in(self):
        """Check for authorization failed error without any token"""
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logged_with_invalid_token(self):
        """Check if validates with invalid token"""
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token + 'x')
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_time_expiration(self):
        """Check for expired token"""
        exp = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)
        payload = jwt_get_payload(self.user, exp=exp)
        token = jwt_encode_payload(payload)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertRegexpMatches(res.data['detail'], 'Token expired')

    def test_valid_user(self):
        """Check if user profile is responded for authenticated token"""
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = self.client.get(PROFILE_URL)
        del self.user_dict['password']
        self.user_dict['user_id'] = res.data['user_id']
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, self.user_dict)


class JwksEndpointTest(TestCase):
    """Test jwks endpoint"""

    def test_endpoint_response(self):
        """Check if jwks endpoint give at least a jwk"""
        self.client = APIClient()
        res = self.client.get(JWKS_URL).json()
        jwks = res['keys']
        self.assertGreaterEqual(len(jwks), 1)
    
