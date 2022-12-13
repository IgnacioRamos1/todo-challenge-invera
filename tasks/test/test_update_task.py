from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import json

from tasks.models import Task


class UpdateTaskTestCase(TestCase):
    def setUp(self):
        user1 = User(
            username='testing_login@testing.com',
        )
        user1.set_password('testing123')
        user1.save()
        
        user2 = User(
            username='testing_login_2@testing.com',
        )
        user2.set_password('testing123')
        user2.save()

        task = Task(
            owner=user1,
            id=1,
            title='testing_get_task',
            description='testing_get_task',
            complete=False,
            expiration_date=timezone.now()
        )
        task.save()

        self.client_login = APIClient()
        response_login = self.client_login.post(
            '/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response_login.content)

        self.client_login.credentials(
            HTTP_AUTHORIZATION='Bearer ' + result['access']
            )

        response_login_2 = self.client_login.post(
            '/login/', {
                "username": "testing_login_2@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        self.result_2 = json.loads(response_login_2.content)
        
        self.date = timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def test_update_task(self):
        client = self.client_login

        response_update_task = client.patch(
            '/tasks/1/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": self.date
            },
            format='json'
        )

        response_get_updated_task = client.get(
            '/tasks/', {
            },
            format='json'
        )

        result = json.loads(response_get_updated_task.content)

        self.assertEqual(
            response_update_task.status_code,
            status.HTTP_200_OK
            )
        self.assertEqual(
            result[0]['title'],
            'testing_update_task'
            )
        self.assertEqual(
            result[0]['description'],
            'testing_update_task'
            )
        self.assertEqual(
            result[0]['complete'],
            True
            )
        self.assertEqual(
            result[0]['expiration_date'],
            self.date
            )


    def test_update_task_not_found(self):
        client = self.client_login

        response_update_task = client.patch(
            '/tasks/2/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": self.date
            },
            format='json'
        )

        self.assertEqual(
            response_update_task.status_code,
            status.HTTP_404_NOT_FOUND
            )

    def test_update_task_without_token(self):
        client = self.client_login

        client.credentials()

        response_update_task = client.patch(
            '/tasks/1/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": self.date
            },
            format='json'
        )

        self.assertEqual(
            response_update_task.status_code,
            status.HTTP_401_UNAUTHORIZED
            )

    def test_update_task_with_invalid_token(self):
        client = self.client_login

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')

        response_update_task = client.patch(
            '/tasks/1/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": self.date
            },
            format='json'
        )

        self.assertEqual(
            response_update_task.status_code,
            status.HTTP_401_UNAUTHORIZED
            )

    def test_update_task_without_ownership(self):
        client = self.client_login
        self.client_login.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.result_2['access']
            )
        response_update_task = client.patch(
            '/tasks/1/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": self.date
            },
            format='json'
        )


        self.assertEqual(
            response_update_task.status_code,
            status.HTTP_403_FORBIDDEN
            )
        self.assertEqual(
            response_update_task.data['message'],
            'You are not the owner of this task.'
        )
