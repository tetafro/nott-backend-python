from django.test import TestCase


class HealthTestCase(TestCase):
    def test_healthz(self):
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
