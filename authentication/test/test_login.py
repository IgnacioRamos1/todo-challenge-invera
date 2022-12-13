from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
import json


class UserLoginTestCase(TestCase):
    def setUp(self):
        user = User(
            username='testing_login@testing.com',
        )
        user.set_password('testing123')
        user.save()

    def test_user_login(self):
        response = APIClient().post(
            '/auth/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', result)
        self.assertIn('refresh', result)

    def test_wrong_user_login(self):
        response = APIClient().post(
            '/auth/login/', {
                "username": "testing@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['detail'],
            'No active account found with the given credentials'
            )

    def test_wrong_password_login(self):
        response = APIClient().post(
            '/auth/login/', {
                "username": "testing@testing.com",
                "password": "testing"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['detail'],
            'No active account found with the given credentials'
            )

    def test_no_username_login(self):
        response = APIClient().post(
            '/auth/login/', {
                "password": "testing123"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['username'],
            ['This field is required.']
            )

    def test_no_password_login(self):
        response = APIClient().post(
            '/auth/login/', {
                "username": "testing@testing.com"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['password'],
            ['This field is required.']
            )
