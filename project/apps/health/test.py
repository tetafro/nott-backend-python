import logging

from django.test import TestCase


logging.disable(logging.CRITICAL)


class HealthTestCase(TestCase):
    def test_healthz(self):
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
