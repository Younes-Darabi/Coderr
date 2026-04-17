from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from reviews.models import Review
from user_auth.models import CustomUser


class OfferTestBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.business_user = CustomUser.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="business"
        )
        cls.customer_user = CustomUser.objects.create_user(
            username="exampleUsername2",
            email="example2@mail.de",
            password="examplePassword2",
            type="customer"
        )
        cls.customer_user_2 = CustomUser.objects.create_user(
            username="exampleUsername4",
            email="example4@mail.de",
            password="examplePassword4",
            type="customer"
        )
        cls.reviews = Review.objects.create(
            reviewer = cls.customer_user,
            business_user = cls.business_user,
            rating = '4',
            description = 'Noch besser als erwartet!'
        )


class ReviewPostTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('review')
        self.client.force_authenticate(user=self.customer_user_2)
        self.data = {
            "business_user": 1,
            "rating": 4,
            "description": "Alles war toll!"
        }
        self.data_error = {
            "rating": 4,
            "description": "Alles war toll!"
        }

    def test_successful(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful(self):
        response = self.client.post(self.url, self.data_error, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_customer_user(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewGetTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('review')
        self.client.force_authenticate(user=self.customer_user)

    def test_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewPatchTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('review-detail', kwargs={'pk': 1})
        self.url_Error = reverse('review-detail', kwargs={'pk': 10})
        self.client.force_authenticate(user=self.customer_user)
        self.data = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        self.data_error = {
            "rating": None,
        }

    def test_successful(self):
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful(self):
        response = self.client.patch(self.url, self.data_error, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_creator(self):
        self.client.force_authenticate(user=self.customer_user_2)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(self.url_Error, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReviewDeleteTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('review-detail', kwargs={'pk': 1})
        self.url_Error = reverse('review-detail', kwargs={'pk': 10})
        self.client.force_authenticate(user=self.customer_user)

    def test_successful(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_creater(self):
        self.client.force_authenticate(user=self.customer_user_2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(self.url_Error)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
