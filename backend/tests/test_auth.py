"""
Authentication tests.
"""

from django.urls import reverse

from rest_framework.test import (
    APITestCase
)

from rest_framework import status

from apps.accounts.models import User


class AuthenticationTests(
    APITestCase
):

    def test_user_registration(self):

        response = self.client.post(

            "/api/accounts/register/",

            {

                "email":
                "new@test.com",

                "username":
                "newuser",

                "password":
                "Password123!"
            },

            format="json"
        )

        self.assertEqual(

            response.status_code,

            status.HTTP_201_CREATED
        )

    def test_jwt_token(self):

        User.objects.create_user(

            email="user@test.com",

            username="user",

            password="Password123!"
        )

        response = self.client.post(

            "/api/token/",

            {

                "email":
                "user@test.com",

                "password":
                "Password123!"
            }
        )

        self.assertEqual(

            response.status_code,

            status.HTTP_200_OK
        )

        self.assertIn(
            "access",
            response.data
        )