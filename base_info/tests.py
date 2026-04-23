from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class BaseInfoGetTest(APITestCase):
    """
    Tests the base-info endpoint to ensure statistics are accessible publicly.
    """

    def test_successful(self):
        """
        Verifies that any user (authenticated or not) can retrieve general platform stats.
        """
        self.url = reverse('base-info')
        response = self.client.get(self.url)

        """ Should return 200 OK regardless of authentication """
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """ Verify the structure of the returned data """
        self.assertIn('review_count', response.data)
        self.assertIn('average_rating', response.data)
