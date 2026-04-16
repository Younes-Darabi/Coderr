from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from offers.models import Offer, OfferDetail
from user_auth.models import CustomUser
from orders.models import Order


class OfferTestBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.business_user = CustomUser.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="business-user"
        )
        cls.customer_user = CustomUser.objects.create_user(
            username="exampleUsername2",
            email="example2@mail.de",
            password="examplePassword2",
            type="customer"
        )
        cls.superuser = CustomUser.objects.create_superuser(
            username="exampleUsername3",
            email="example3@mail.de",
            password="examplePassword3",
        )
        cls.offer = Offer.objects.create(
            title="Grafikdesign-Paket",
            description="Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            image=None,
            creator=cls.customer_user
        )
        cls.offer_detail = OfferDetail.objects.create(
            offer=cls.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )
        cls.order = Order.objects.create(
            offer_detail=cls.offer_detail,
            customer_user=cls.customer_user,
            business_user=cls.business_user
        )

class OrderPostTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('order')
        self.client.force_authenticate(user=self.customer_user)
        self.data = {
            "offer_detail_id": 1
        }
        self.data_error = {
            "aaaaaaaa": 1
        }

        self.data_not_found = {
            "offer_detail_id": 10
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

    def test_not_founf(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(self.url, self.data_not_found, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderGetTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('order')
        self.client.force_authenticate(user=self.customer_user)

    def test_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class orderDetailPatchTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('order-detail', kwargs={'pk': 1})
        self.url_Error = reverse('order-detail', kwargs={'pk': 10})
        self.client.force_authenticate(user=self.business_user)
        self.data = {
            "status": "completed"
        }
        self.data_error = {
            "status": None,
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
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        response = self.client.patch(self.url_Error, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderDeleteTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('order-detail', kwargs={'pk': 1})
        self.url_Error = reverse('order-detail', kwargs={'pk': 10})
        self.client.force_authenticate(user=self.superuser)

    def test_successful(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_superuser(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.url_Error)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderCountGetTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('order-count', kwargs={'pk': 1})
        self.url_Error = reverse('order-count', kwargs={'pk': 10})
        self.client.force_authenticate(user=self.customer_user)

    def test_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.url_Error)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CompletedOrderCountGetTest(OfferTestBase):

    def setUp(self):
        self.url = reverse('completed-order-count', kwargs={'pk': 1})
        self.url_Error = reverse('completed-order-count', kwargs={'pk': 10})
        self.client.force_authenticate(user=self.customer_user)

    def test_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.url_Error)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)