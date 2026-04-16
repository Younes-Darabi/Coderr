# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from .models import CustomUser


# class RegistrationTest(APITestCase):

#     def setUp(self):
#         self.url = reverse('register')
#         self.valid_data = {
#             "username": "exampleUsername",
#             "email": "example@mail.de",
#             "password": "examplePassword",
#             "repeated_password": "examplePassword",
#             "type": "customer"
#         }
#         self.invalid_data = {
#             "username": "exampleUsername",
#             "email": "example@mail.de",
#             "password": "examplePassword",
#             "repeated_password": "examplePassword",
#         }
#         self.invalid_data_mismatched_password = {
#             "username": "exampleUsername",
#             "email": "example@mail.de",
#             "password": "examplePassword1",
#             "repeated_password": "examplePassword2",
#             "type": "customer"
#         }

#     def test_successful_registration(self):
#         response = self.client.post(self.url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_missing_type(self):
#         response = self.client.post(self.url, self.invalid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_password_mismatch(self):
#         response = self.client.post(self.url, self.invalid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class LoginTest(APITestCase):

#     def setUp(self):
#         self.url = reverse('login')
#         CustomUser.objects.create_user(
#             username="exampleUsername",
#             email="example@mail.de",
#             password="examplePassword",
#             type="customer"
#         )
#         self.valid_data = {
#             "username": "exampleUsername",
#             "password": "examplePassword",
#         }
#         self.invalid_data = {
#             "username": "exampleUsername",
#             "email": "example@mail.de",
#         }
#         self.invalid_data_password = {
#             "username": "exampleUsername",
#             "password": "123456789",
#         }

#     def test_successful_login(self):
#         response = self.client.post(self.url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_missing_password(self):
#         response = self.client.post(self.url, self.invalid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_Wrong_password(self):
#         response = self.client.post(
#             self.url, self.invalid_data_password, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
