from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
import json


class UserTestCase(TestCase):
    def setUp(self):
        user = User(
            username='testing_login@testing.com',
        )
        user.set_password('testing123')
        user.save()

        self.client_logout = APIClient()
        response_login = self.client_logout.post(
            '/auth/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        self.result = json.loads(response_login.content)

        self.client_logout.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.result['access']
            )

    def test_user_logout(self):
        response_logout = self.client_logout.post(
            '/auth/logout/', {
                "refresh_token": self.result['refresh'],
            },
            format='json'
        )
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_logout.data['detail'],
            'Logged out successfully'
            )

    def test_user_logout_without_refresh_token(self):
        self.client_logout.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.result['access']
            )

        response_logout = self.client_logout.post(
            '/auth/logout/', {
            },
            format='json'
        )
        self.assertEqual(
            response_logout.status_code,
            status.HTTP_400_BAD_REQUEST
            )
        self.assertEqual(
            response_logout.data['detail'],
            'Refresh token is required'
            )

    def test_user_logout_without_token(self):
        self.client_logout.credentials()

        response_logout = self.client_logout.post(
            '/auth/logout/', {
                "refresh_token": self.result['refresh'],
            },
            format='json'
        )
        self.assertEqual(
            response_logout.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        self.assertEqual(
            response_logout.data['detail'],
            'Authentication credentials were not provided.'
            )

    def test_user_logout_with_all(self):
        response_logout = self.client_logout.post(
            '/auth/logout/', {
                "all": True,
            },
            format='json'
        )
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_logout.data['detail'],
            'All refresh tokens have been blacklisted'
            )

    def test_user_logout_get_new_token(self):
        self.client_logout.post(
            '/auth/logout/', {
                "refresh_token": self.result['refresh'],
            },
            format='json'
        )

        response_login_refresh = self.client_logout.post(
            '/auth/login/refresh/', {
                "refresh": self.result['refresh'],
            },
            format='json'
        )
        self.assertEqual(
            response_login_refresh.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        self.assertEqual(
            response_login_refresh.data['detail'],
            'Token is blacklisted'
            )
