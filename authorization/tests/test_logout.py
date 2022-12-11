from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import json


class UserTestCase(TestCase):
    def setUp(self):
        user = User(
            username = 'testing_login@testing.com',
        )
        user.set_password('testing123')
        user.save()

    def test_user_logout(self):
        client = APIClient()
        response_login = client.post(
            '/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response_login.content)
        
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + result['access'])

        response_logout = client.post(
            '/logout/', {
                "refresh_token": result['refresh'],
            },
            format='json'
        )
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
        self.assertEqual(response_logout.data['status'], 'OK, goodbye')
    
    def test_user_logout_without_refresh_token(self):
        client = APIClient()
        response_login = client.post(
            '/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response_login.content)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + result['access'])

        response_logout = client.post(
            '/logout/', {
            },
            format='json'
        )
        self.assertEqual(response_logout.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_logout.data['detail'], 'Refresh token is required')

    
    def test_user_logout_without_token(self):
        client = APIClient()
        response_login = client.post(
            '/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response_login.content)

        response_logout = client.post(
            '/logout/', {
                "refresh_token": result['refresh'],
            },
            format='json'
        )
        self.assertEqual(response_logout.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_logout.data['detail'], 'Authentication credentials were not provided.')

    def test_user_logout_with_all(self):
        client = APIClient()
        response_login = client.post(
            '/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response_login.content)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + result['access'])

        response_logout = client.post(
            '/logout/', {
                "all": True,
            },
            format='json'
        )
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
        self.assertEqual(response_logout.data['status'], 'OK, goodbye, all refresh tokens blacklisted')

    def test_user_logout_get_new_token(self):
        client = APIClient()
        response_login = client.post(
            '/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response_login.content)
        
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + result['access'])

        response_logout = client.post(
            '/logout/', {
                "refresh_token": result['refresh'],
            },
            format='json'
        )

        response_login_refresh = client.post(
            '/login/refresh/', {
                "refresh": result['refresh'],
            },
            format='json'
        )
        self.assertEqual(response_login_refresh.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_login_refresh.data['detail'], 'Token is blacklisted')
