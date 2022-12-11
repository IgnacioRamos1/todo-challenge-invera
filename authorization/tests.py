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

    def test_user_registration(self):
        client = APIClient()
        response = client.post(
            '/register/', {
                "username": "testing@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User Created Successfully.  Now perform Login to get your token')
        self.assertEqual(response.data['user']['username'], 'testing@testing.com')

    def test_user_login(self):
        client = APIClient()
        response = client.post(
            '/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', result)
        self.assertIn('refresh', result)

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
