from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from user_auth.models import CustomUser


class ProfileGetTest(APITestCase):
    """
    Tests the GET functionality for individual user profiles.
    Verifies retrieval, authentication requirements, and error handling for missing profiles.
    """

    def setUp(self):
        """
        Sets up a test user and authenticates the client before each test.
        """
        self.url = reverse('profile-detail', kwargs={'pk': 1})
        self.user = CustomUser.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="customer"
        )
        self.client.force_authenticate(user=self.user)

    def test_successful(self):
        """
        Tests successful profile retrieval for an authenticated user.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        """
        Tests that an unauthenticated user cannot access profile details.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        """
        Tests the response when a profile ID does not exist in the database.
        """
        self.url = reverse('profile-detail', kwargs={'pk': 2})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProfilePatchTest(APITestCase):
    """
    Tests the PATCH (partial update) functionality for user profiles.
    Ensures users can only edit their own profile data.
    """

    def setUp(self):
        """
        Prepares test users (owner and non-owner) and sample update data.
        """
        self.url = reverse('profile-detail', kwargs={'pk': 1})
        self.user = CustomUser.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="customer"
        )
        self.user2 = CustomUser.objects.create_user(
            username="exampleUsername2",
            email="example2@mail.de",
            password="examplePassword2",
            type="business"
        )
        self.data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
        self.client.force_authenticate(user=self.user)

    def test_successful(self):
        """
        Tests that a user can successfully update their own profile.
        """
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        """
        Ensures updates are rejected if the requester is not logged in.
        """
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_user_profile(self):
        """
        Ensures a user cannot update another user's profile (IsOwner permission check).
        """
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        """
        Tests the response when attempting to update a non-existent profile ID.
        """
        self.url = reverse('profile-detail', kwargs={'pk': 3})
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BusinessProfileGetTest(APITestCase):
    """
    Tests the list view for all Business-type profiles.
    """

    def setUp(self):
        self.url = reverse('profile-business')
        self.user = CustomUser.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="customer"
        )
        self.client.force_authenticate(user=self.user)

    def test_successful(self):
        """
        Verifies that authenticated users can list business profiles.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        """
        Verifies that access is denied for anonymous users.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomerProfileGetTest(APITestCase):
    """
    Tests the list view for all Customer-type profiles.
    """

    def setUp(self):
        self.url = reverse('profile-customer')
        self.user = CustomUser.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="customer"
        )
        self.client.force_authenticate(user=self.user)

    def test_successful(self):
        """
        Verifies that authenticated users can list customer profiles.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        """
        Verifies that access is denied for anonymous users.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
