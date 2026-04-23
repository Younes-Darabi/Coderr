from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user_auth.models import CustomUser


class ProfileGetTest(APITestCase):

    def setUp(self):
        self.url = reverse('profile-detail', kwargs={'pk': 1})
        self.user = CustomUser.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="customer"
        )
        self.client.force_authenticate(user=self.user)

    def test_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        self.url = reverse('profile-detail', kwargs={'pk': 2})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProfilePatchTest(APITestCase):

    def setUp(self):
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
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_user_profile(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        self.url = reverse('profile-detail', kwargs={'pk': 3})
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BusinessProfileGetTest(APITestCase):

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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomerProfileGetTest(APITestCase):

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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
