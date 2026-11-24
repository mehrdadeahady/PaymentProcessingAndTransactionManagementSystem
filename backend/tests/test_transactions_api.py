"""
Transfer API tests.
"""

from decimal import Decimal

from rest_framework.test import (
    APITestCase
)

from rest_framework import status

from apps.accounts.models import User
from apps.wallets.models import Wallet


class TransferApiTests(
    APITestCase
):

    def setUp(self):

        self.sender = (
            User.objects.create_user(

                email="sender@test.com",

                username="sender",

                password="Password123!"
            )
        )

        self.receiver = (
            User.objects.create_user(

                email="receiver@test.com",

                username="receiver",

                password="Password123!"
            )
        )

        Wallet.objects.create(

            user=self.sender,

            balance=Decimal("1000.00")
        )

        Wallet.objects.create(

            user=self.receiver,

            balance=Decimal("0.00")
        )

        login = self.client.post(

            "/api/token/",

            {

                "email":
                "sender@test.com",

                "password":
                "Password123!"
            }
        )

        token = login.data["access"]

        self.client.credentials(

            HTTP_AUTHORIZATION=
            f"Bearer {token}"
        )

    def test_transfer_creation(self):

        response = self.client.post(

            "/api/transactions/transfer/",

            {

                "receiver_id":
                self.receiver.id,

                "amount":
                "100.00"
            },

            format="json"
        )

        self.assertEqual(

            response.status_code,

            status.HTTP_201_CREATED
        )

        self.assertIn(

            "transaction_id",

            response.data
        )