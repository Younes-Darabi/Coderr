from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import CustomUser


class RegistrationTest(APITestCase):
    """
    Test suite for user registration functionality.
    Verifies that users can register with valid data and 
    checks error handling for incomplete or mismatched data.
    """

    def setUp(self):
        """
        Initializes the test environment, URLs, and sample datasets 
        for registration scenarios.
        """
        self.url = reverse('register')

        # Valid data for successful registration
        self.valid_data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }

        # Invalid data missing the required 'type' field
        self.invalid_data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
        }

        # Invalid data where password and repeated_password do not match
        self.invalid_data_mismatched_password = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword1",
            "repeated_password": "examplePassword2",
            "type": "customer"
        }

    def test_successful_registration(self):
        """
        Tests that a user is successfully created when provided with valid input.
        Expects HTTP 201 Created.
        """
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_type(self):
        """
        Tests that registration fails when the user type is missing.
        Expects HTTP 400 Bad Request.
        """
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_mismatch(self):
        """
        Tests that registration fails when passwords do not match.
        Expects HTTP 400 Bad Request.
        """
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(APITestCase):
    """
    Test suite for user authentication (Login).
    Ensures users can log in with correct credentials and 
    handles incorrect or missing data appropriately.
    """

    def setUp(self):
        """
        Sets up a test user in the temporary database and prepares
        the login URL and test payloads.
        """
        self.url = reverse('login')

        # Pre-create a user to test authentication
        CustomUser.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="customer"
        )

        # Credentials for successful login
        self.valid_data = {
            "username": "exampleUsername",
            "password": "examplePassword",
        }

        # Credentials missing the password field
        self.invalid_data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
        }

        # Credentials with an incorrect password
        self.invalid_data_password = {
            "username": "exampleUsername",
            "password": "123456789",
        }

    def test_successful_login(self):
        """
        Tests that a user can log in with correct credentials.
        Expects HTTP 200 OK.
        """
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_missing_password(self):
        """
        Tests that login fails if the password field is not provided.
        Expects HTTP 400 Bad Request.
        """
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Wrong_password(self):
        """
        Tests that login fails if the provided password is incorrect.
        Expects HTTP 400 Bad Request.
        """
        response = self.client.post(
            self.url, self.invalid_data_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
