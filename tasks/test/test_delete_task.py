from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import json

from tasks.models import Task


class DeleteTaskTestCase(TestCase):
    def setUp(self):
        date = timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ")

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

        response_login_2 = self.client_login.post(
            '/auth/login/', {
                "username": "testing_login_2@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        self.result_2 = json.loads(response_login_2.content)

    def test_delete_task(self):
        response_delete_task = self.client_login.delete(
            '/tasks/1/', {
            },
            format='json'
        )

        response_get_task = self.client_login.get(
            '/tasks/', {
            },
            format='json'
        )

        self.assertEqual(
            response_delete_task.status_code,
            status.HTTP_204_NO_CONTENT
            )
        self.assertEqual(len(response_get_task.data), 0)
        self.assertEqual(response_delete_task.data['detail'], 'Task deleted successfully.')

    def test_delete_task_not_found(self):
        response_delete_task = self.client_login.delete(
            '/tasks/2/', {
            },
            format='json'
        )

        self.assertEqual(
            response_delete_task.status_code,
            status.HTTP_404_NOT_FOUND
            )
        self.assertEqual(response_delete_task.data['detail'], 'Not found.')

    def test_delete_task_without_token(self):
        self.client_login.credentials()

        response_delete_task = self.client_login.delete(
            '/tasks/1/', {
            },
            format='json'
        )

        self.assertEqual(
            response_delete_task.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        self.assertEqual(
            response_delete_task.data['detail'],
            'Authentication credentials were not provided.'
            )

    def test_delete_task_with_invalid_token(self):
        self.client_login.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')

        response_delete_task = self.client_login.delete(
            '/tasks/1/', {
            },
            format='json'
        )

        self.assertEqual(
            response_delete_task.status_code,
            status.HTTP_401_UNAUTHORIZED
            )
        self.assertEqual(
            response_delete_task.data['detail'],
            'Given token not valid for any token type'
            )

    def test_delete_task_without_ownership(self):
        self.client_login.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.result_2['access']
            )

        response_delete_task = self.client_login.delete(
            '/tasks/1/', {
            },
            format='json'
        )

        self.assertEqual(
            response_delete_task.status_code,
            status.HTTP_403_FORBIDDEN
            )
        self.assertEqual(
            response_delete_task.data['detail'],
            'You are not the owner of this task.'
            )
