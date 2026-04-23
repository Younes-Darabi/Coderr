from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from offers.models import Offer, OfferDetail
from user_auth.models import CustomUser


class OfferTestBase(APITestCase):
    """
    Base test class for Offers. 
    Provides shared setup data including business/customer users and sample offer structures.
    """
    @classmethod
    def setUpTestData(cls):
        # Sample data for creating a valid offer with multiple tiers (Basic, Standard, Premium)
        cls.offer_data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        }

        # Incomplete data for testing validation errors
        cls.offer_data_error = {
            "title": "Grafikdesign-Paket",
        }

        # Test users with different roles
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

        # Filtering and ordering parameters for GET requests
        cls.filter = {
            'creator_id': 1,
            'min_price': 100,
            'max_delivery_time': 7,
            'ordering': 'min_price',
            'search': 'Design',
            'page_size': 10
        }
        cls.filter_error = {
            'creator_id': 'A',
        }

        # Create an initial offer in the database for retrieval/update tests
        cls.offer = Offer.objects.create(
            title="Grafikdesign-Paket",
            description="Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            image=None,
            creator=cls.customer_user
        )
        OfferDetail.objects.create(
            offer=cls.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )


class OfferPostTest(OfferTestBase):
    """
    Tests the creation of new offers (POST).
    Verifies permissions (Business only) and data validation.
    """

    def setUp(self):
        self.url = reverse('offer')
        self.client.force_authenticate(user=self.business_user)

    def test_successful(self):
        """Valid business user creating a complete offer."""
        response = self.client.post(self.url, self.offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful(self):
        """Creation fails when required fields are missing."""
        response = self.client.post(
            self.url, self.offer_data_error, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_authenticated(self):
        """Creation fails for anonymous users."""
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, self.offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_business_user(self):
        """Creation fails for customers even if authenticated."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(self.url, self.offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OfferGetTest(OfferTestBase):
    """
    Tests the list view of offers (GET).
    Verifies filtering, searching, and query parameters.
    """

    def setUp(self):
        self.url = reverse('offer')
        self.filter = {'min_price': '50', 'max_delivery_time': '10'}
        self.filter_error = {'min_price': 'abc', 'max_delivery_time': 'xyz'}

    def test_successful(self):
        """Retrieving the full list of offers."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_parameters(self):
        """Retrieving offers using valid filter parameters."""
        response = self.client.get(self.url, self.filter)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful_parameters(self):
        """Expects 400 Bad Request when filter values are non-numeric."""
        response = self.client.get(self.url, self.filter_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OfferDetailGetTest(OfferTestBase):
    """
    Tests retrieving a specific offer by ID (Retrieve).
    """

    def setUp(self):
        self.url = reverse('offer-detail', kwargs={'pk': 1})
        self.url_Error = reverse('offer-detail', kwargs={'pk': 2})
        self.client.force_authenticate(user=self.business_user)

    def test_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        response = self.client.get(self.url_Error)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OfferDetailPatchTest(OfferTestBase):
    """
    Tests partial updates (PATCH) on an existing offer.
    Verifies that only the creator can update the offer.
    """

    def setUp(self):
        self.url = reverse('offer-detail', kwargs={'pk': 1})
        self.url_Error = reverse('offer-detail', kwargs={'pk': 10})
        self.client.force_authenticate(
            user=self.customer_user)  # Creator of 'offer'
        self.data = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "basic"
                }
            ]
        }
        self.data_error = {"title": None}

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
        """Ensures non-creators are forbidden from updating."""
        self.client.force_authenticate(user=self.business_user)
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        response = self.client.patch(self.url_Error, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OfferDeleteTest(OfferTestBase):
    """
    Tests offer deletion (DELETE).
    """

    def setUp(self):
        self.url = reverse('offer-detail', kwargs={'pk': 1})
        self.url_Error = reverse('offer-detail', kwargs={'pk': 10})
        self.client.force_authenticate(user=self.customer_user)

    def test_successful(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_creator(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found(self):
        response = self.client.delete(self.url_Error)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SingleDetailOfferGetTest(OfferTestBase):
    """
    Tests retrieving specific tier details (OfferDetail).
    """

    def setUp(self):
        self.url = reverse('offer-details', kwargs={'pk': 1})
        self.url_Error = reverse('offer-details', kwargs={'pk': 10})
        self.client.force_authenticate(user=self.customer_user)

    def test_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        response = self.client.get(self.url_Error)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
