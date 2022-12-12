from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User
import json

from tasks.models import Task


class DeleteTaskTestCase(TestCase):
    def setUp(self):
        task = Task(
            id=1,
            title='testing_get_task',
            description='testing_get_task',
            complete=False,
            expiration_date='2020-12-12 12:12:12'
        )
        task.save()

        user = User(
            username='testing_login@testing.com',
        )
        user.set_password('testing123')
        user.save()

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

    def test_delete_task(self):
        client = self.client_login

        response_delete_task = client.delete(
            '/tasks/1/', {
            },
            format='json'
        )

        response_get_task = client.get(
            '/tasks/', {
            },
            format='json'
        )

        self.assertEqual(
            response_delete_task.status_code,
            status.HTTP_204_NO_CONTENT
            )
        self.assertEqual(len(response_get_task.data), 0)

    def test_delete_task_not_found(self):
        client = self.client_login

        response_delete_task = client.delete(
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
        client = self.client_login

        client.credentials()

        response_delete_task = client.delete(
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
        client = self.client_login

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')

        response_delete_task = client.delete(
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
