from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from tasks.models import Task

from django.contrib.auth.models import User

import json

class GetTaskTestCase(TestCase):
    def setUp(self):
        task = Task(
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
    
    def test_get_task(self):
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

        response_get_task = client.get(
            '/tasks/', {
            },
            format='json'
        )
        self.assertEqual(response_get_task.status_code, status.HTTP_200_OK)

    def test_get_task_without_token(self):
        client = APIClient()
        response_get_task = client.get(
            '/tasks/', {
            },
            format='json'
        )
        self.assertEqual(response_get_task.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_get_task.data['detail'], 'Authentication credentials were not provided.')

    def test_get_task_with_invalid_token(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response_get_task = client.get(
            '/tasks/', {
            },
            format='json'
        )
        self.assertEqual(response_get_task.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_get_task.data['detail'], 'Given token not valid for any token type')
        self.assertEqual(response_get_task.data['code'], 'token_not_valid')
        self.assertEqual(response_get_task.data['messages'][0]['message'], 'Token is invalid or expired')
