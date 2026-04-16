from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from offers.models import Offer, OfferDetail
from user_auth.models import CustomUser


class OfferTestBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
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
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        cls.offer_data_error = {
            "title": "Grafikdesign-Paket",
        }
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

# class OfferPostTest(OfferTestBase):

    # def setUp(self):
    #     self.url = reverse('offer')
    #     self.client.force_authenticate(user=self.business_user)

    # def test_successful(self):
    #     response = self.client.post(self.url, self.offer_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_unsuccessful(self):
    #     response = self.client.post(self.url, self.offer_data_error, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_not_authenticated(self):
    #     self.client.force_authenticate(user=None)
    #     response = self.client.post(self.url, self.offer_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_not_business_user(self):
    #     self.client.force_authenticate(user=self.customer_user)
    #     response = self.client.post(self.url, self.offer_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class OfferGetTest(OfferTestBase):

#     def setUp(self):
#         self.url = reverse('offer')

#     def test_successful(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_successful_parameters(self):
#         response = self.client.get(self.url, self.filter)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_unsuccessful_parameters(self):
#         response = self.client.get(self.url, self.filter_error)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class OfferDetailGetTest(OfferTestBase):

#     def setUp(self):
#         self.url = reverse('offer-detail', kwargs={'pk': 1})
#         self.url_Error = reverse('offer-detail', kwargs={'pk': 2})
#         self.client.force_authenticate(user=self.business_user)

#     def test_successful(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_not_authenticated(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.get(self.url, self.filter)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_not_found(self):
#         response = self.client.get(self.url_Error, self.filter_error)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class OfferDetailPatchTest(OfferTestBase):

#     def setUp(self):
#         self.url = reverse('offer-detail', kwargs={'pk': 1})
#         self.url_Error = reverse('offer-detail', kwargs={'pk': 2})
#         self.client.force_authenticate(user=self.customer_user)
#         self.data = {
#             "title": "Updated Grafikdesign-Paket",
#             "details": [
#                 {
#                     "title": "Basic Design Updated",
#                     "revisions": 3,
#                     "delivery_time_in_days": 6,
#                     "price": 120,
#                     "features": [
#                         "Logo Design",
#                         "Flyer"
#                     ],
#                     "offer_type": "basic"
#                 }
#             ]
#         }
#         self.data_error = {
#             "title": None,
#         }

#     def test_successful(self):
#         response = self.client.patch(self.url, self.data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_unsuccessful(self):
#         response = self.client.patch(self.url, self.data_error, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_not_authenticated(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.patch(self.url, self.data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_not_creator(self):
#         self.client.force_authenticate(user=self.business_user)
#         response = self.client.patch(self.url, self.data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_not_found(self):
#         response = self.client.patch(self.url_Error, self.data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class OfferDetailDeleteTest(OfferTestBase):

#     def setUp(self):
#         self.url = reverse('offer-detail', kwargs={'pk': 1})
#         self.url_Error = reverse('offer-detail', kwargs={'pk': 2})
#         self.client.force_authenticate(user=self.customer_user)
#         self.data = {
#             "title": "Updated Grafikdesign-Paket",
#             "details": [
#                 {
#                     "title": "Basic Design Updated",
#                     "revisions": 3,
#                     "delivery_time_in_days": 6,
#                     "price": 120,
#                     "features": [
#                         "Logo Design",
#                         "Flyer"
#                     ],
#                     "offer_type": "basic"
#                 }
#             ]
#         }
#         self.data_error = {
#             "title": None,
#         }

#     def test_successful(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_not_authenticated(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_not_creator(self):
#         self.client.force_authenticate(user=self.business_user)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_not_found(self):
#         self.client.force_authenticate(user=self.customer_user)
#         response = self.client.delete(self.url_Error)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class SingleDetailOfferGetTest(OfferTestBase):

#     def setUp(self):
#         self.url = reverse('offer-details', kwargs={'pk': 1})
#         self.url_Error = reverse('offer-details', kwargs={'pk': 2})
#         self.client.force_authenticate(user=self.customer_user)
#         self.data = {
#             "title": "Updated Grafikdesign-Paket",
#             "details": [
#                 {
#                     "title": "Basic Design Updated",
#                     "revisions": 3,
#                     "delivery_time_in_days": 6,
#                     "price": 120,
#                     "features": [
#                         "Logo Design",
#                         "Flyer"
#                     ],
#                     "offer_type": "basic"
#                 }
#             ]
#         }
#         self.data_error = {
#             "title": None,
#         }

#     def test_successful(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_not_authenticated(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_not_found(self):
#         self.client.force_authenticate(user=self.customer_user)
#         response = self.client.get(self.url_Error)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)