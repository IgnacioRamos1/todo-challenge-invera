from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json

class LogsTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_critical_logs(self):
        client = APIClient()
        response = client.get(
            '/logs/critical/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_error_logs(self):
        client = APIClient()
        response = client.get(
            '/logs/error/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_warning_logs(self):
        client = APIClient()
        response = client.get(
            '/logs/warning/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_info_logs(self):
        client = APIClient()
        response = client.get(
            '/logs/info/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_debug_logs(self):
        client = APIClient()
        response = client.get(
            '/logs/debug/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
