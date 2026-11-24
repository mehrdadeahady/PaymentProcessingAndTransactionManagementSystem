"""
Wallet tests.
"""

from decimal import Decimal

from django.test import TestCase

from apps.accounts.models import User
from apps.wallets.models import Wallet


class WalletTests(
    TestCase
):

    def test_wallet_creation(self):

        user = (
            User.objects.create_user(

                email="wallet@test.com",

                username="wallet",

                password="Password123!"
            )
        )

        wallet = Wallet.objects.create(

            user=user,

            balance=Decimal("0.00")
        )

        self.assertEqual(

            wallet.balance,

            Decimal("0.00")
        )
