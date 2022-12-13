from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

import json


class CreateTaskTestCase(TestCase):
    def setUp(self):
        self.user = User(
            username='testing_login@testing.com',
        )
        self.user.set_password('testing123')
        self.user.save()

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

        self.date = timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def test_create_task(self):
        response_create_task = self.client_login.post(
            '/tasks/', {
                "owner": self.user.id,
                "title": "testing_create_task",
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": self.date
            },
            format='json'
        )
        
        response_get_task = self.client_login.get(
            '/tasks/', {
            },
            format='json'
        )
        self.assertEqual(
            response_create_task.status_code,
            status.HTTP_201_CREATED
            )
        self.assertEqual(
            response_get_task.data[0]['title'],
            'testing_create_task'
            )
        self.assertEqual(
            response_get_task.data[0]['description'],
            'testing_create_task'
            )
        self.assertEqual(response_get_task.data[0]['complete'], False)
        self.assertEqual(
            response_get_task.data[0]['expiration_date'],
            self.date
            )

    def test_create_task_without_token(self):
        self.client_login.credentials()

        response_create_task = self.client_login.post(
            '/tasks/', {
                "owner": self.user.id,
                "title": "testing_create_task",
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": self.date
            },
            format='json'
        )
        self.assertEqual(
            response_create_task.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        self.assertEqual(
            response_create_task.data['detail'],
            'Authentication credentials were not provided.'
            )

    def test_create_task_with_invalid_token(self):
        self.client_login.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response_create_task = self.client_login.post(
            '/tasks/', {
                "owner": self.user.id,
                "title": "testing_create_task",
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": self.date
            },
            format='json'
        )
        self.assertEqual(
            response_create_task.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        self.assertEqual(
            response_create_task.data['detail'],
            'Given token not valid for any token type'
            )

    def test_create_task_with_no_title(self):
        response_create_task = self.client_login.post(
            '/tasks/', {
                "owner": self.user.id,
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": self.date
            },
            format='json'
        )
        self.assertEqual(
            response_create_task.status_code, status.HTTP_400_BAD_REQUEST
            )
        self.assertEqual(
            response_create_task.data['title'][0],
            'This field is required.'
            )

    def test_create_task_with_too_long_title(self):
        response_create_task = self.client_login.post(
            '/tasks/', {
                "owner": self.user.id,
                "title": "testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task__",
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": self.date
            },
            format='json'
        )
        self.assertEqual(
            response_create_task.status_code,
            status.HTTP_400_BAD_REQUEST
            )
        self.assertEqual(
            response_create_task.data['title'][0],
            'Title is too long.'
            )
