from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import json

from tasks.models import Task

class GetTaskTestCase(TestCase):
    def setUp(self):
        date = timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        user = User(
            username='testing_login@testing.com',
        )
        user.set_password('testing123')
        user.save()

        task = Task(
            owner=user,
            id=1,
            title='testing_get_task',
            description='testing_get_task',
            complete=False,
            expiration_date=date
        )
        task.save()


        self.client_login = APIClient()
        response_login = self.client_login.post(
            '/auth/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response_login.content)

        self.client_login.credentials(
            HTTP_AUTHORIZATION='Bearer ' + result['access']
            )

    def test_get_task(self):
        response_get_task = self.client_login.get(
            '/tasks/', {
            },
            format='json'
        )
        self.assertEqual(response_get_task.status_code, status.HTTP_200_OK)

    def test_get_task_without_token(self):
        self.client_login.credentials()

        response_get_task = self.client_login.get(
            '/tasks/', {
            },
            format='json'
        )
        self.assertEqual(
            response_get_task.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        self.assertEqual(
            response_get_task.data['detail'],
            'Authentication credentials were not provided.'
            )

    def test_get_task_with_invalid_token(self):
        self.client_login.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')

        response_get_task = self.client_login.get(
            '/tasks/', {
            },
            format='json'
        )
        self.assertEqual(
            response_get_task.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        self.assertEqual(
            response_get_task.data['detail'],
            'Given token not valid for any token type'
            )
        self.assertEqual(response_get_task.data['code'], 'token_not_valid')
        self.assertEqual(
            response_get_task.data['messages'][0]['message'],
            'Token is invalid or expired'
            )
