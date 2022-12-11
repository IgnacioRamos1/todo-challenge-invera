from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from tasks.models import Task

from django.contrib.auth.models import User

import json

class UpdateTaskTestCase(TestCase):
    def setUp(self):
        task = Task(
            id = 1,
            title = 'testing_get_task',
            description = 'testing_get_task',
            complete = False,
            expiration_date = '2020-12-12 12:12:12'
        )
        task.save()
    
        user = User(
            username = 'testing_login@testing.com',
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

        self.client_login.credentials(HTTP_AUTHORIZATION='Bearer ' + result['access'])
    
    def test_update_task(self):
        client = self.client_login

        response_update_task = client.patch(
            '/tasks/1/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )

        response_get_task = client.get(
            '/tasks/', {
            },
            format='json'
        )

        self.assertEqual(response_update_task.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get_task.data[0]['title'], 'testing_update_task')
        self.assertEqual(response_get_task.data[0]['description'], 'testing_update_task')
        self.assertEqual(response_get_task.data[0]['complete'], True)
        self.assertEqual(response_get_task.data[0]['expiration_date'], '2020-12-12T12:12:12Z')

    def test_update_task_not_found(self):
        client = self.client_login

        response_update_task = client.patch(
            '/tasks/2/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )

        self.assertEqual(response_update_task.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_task_without_token(self):
        client = self.client_login

        client.credentials()

        response_update_task = client.patch(
            '/tasks/1/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )

        self.assertEqual(response_update_task.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task_with_invalid_token(self):
        client = self.client_login

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')

        response_update_task = client.patch(
            '/tasks/1/', {
                "title": "testing_update_task",
                "description": "testing_update_task",
                "complete": True,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )

        self.assertEqual(response_update_task.status_code, status.HTTP_401_UNAUTHORIZED)
