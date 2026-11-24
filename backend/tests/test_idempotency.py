"""
Most important fintech test.

Verifies duplicate requests
do not generate duplicate
transactions.
"""

from decimal import Decimal

from django.test import TestCase

from apps.accounts.models import User
from apps.wallets.models import Wallet

from apps.transactions.services import (
    create_transaction
)


class IdempotencyTests(
    TestCase
):

    def test_same_key_same_transaction(
        self
    ):

        sender = (
            User.objects.create_user(
                email="s@test.com",
                username="s",
                password="Password123!"
            )
        )

        receiver = (
            User.objects.create_user(
                email="r@test.com",
                username="r",
                password="Password123!"
            )
        )

        Wallet.objects.create(
            user=sender,
            balance=Decimal("1000.00")
        )

        Wallet.objects.create(
            user=receiver,
            balance=Decimal("0.00")
        )

        key = (
            "22222222-2222-2222-2222-222222222222"
        )

        tx1 = create_transaction(

            sender=sender,

            receiver=receiver,

            amount=Decimal("100.00"),

            idempotency_key=key
        )

        tx2 = create_transaction(

            sender=sender,

            receiver=receiver,

            amount=Decimal("100.00"),

            idempotency_key=key
        )

        self.assertEqual(
            tx1.id,
            tx2.id
        )