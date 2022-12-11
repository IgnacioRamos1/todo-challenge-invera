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
        user.set_password('testing')
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
