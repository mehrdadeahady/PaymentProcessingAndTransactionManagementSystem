"""
Tests for transaction service layer.
"""

from decimal import Decimal

from django.test import TestCase

from apps.accounts.models import User
from apps.wallets.models import Wallet
from apps.transactions.models import Transaction

from apps.transactions.services import (
    create_transaction,
    validate_transfer,
    validate_sufficient_balance,
    InvalidTransferException,
    InsufficientFundsException,
)


class TransactionServiceTests(
    TestCase
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

    def test_create_transaction(self):

        tx = create_transaction(

            sender=self.sender,

            receiver=self.receiver,

            amount=Decimal("100.00"),

            idempotency_key=
            "11111111-1111-1111-1111-111111111111"
        )

        self.assertEqual(

            tx.status,

            Transaction.Status.PENDING
        )

    def test_cannot_transfer_to_self(self):

        with self.assertRaises(
            InvalidTransferException
        ):

            validate_transfer(

                sender=self.sender,

                receiver=self.sender,

                amount=Decimal("10.00")
            )

    def test_zero_amount_invalid(self):

        with self.assertRaises(
            InvalidTransferException
        ):

            validate_transfer(

                sender=self.sender,

                receiver=self.receiver,

                amount=Decimal("0.00")
            )

    def test_insufficient_balance(self):

        with self.assertRaises(
            InsufficientFundsException
        ):

            validate_sufficient_balance(

                sender=self.receiver,

                amount=Decimal("500.00")
            )