"""
Tests for transaction tasks.

Focus:

✓ Success path

✓ Retry path

✓ Permanent failure path

✓ Wallet updates

✓ Audit logging
"""

# Mock framework.
from unittest.mock import patch

# Monetary values.
from decimal import Decimal

# Django testing tools.
from django.test import (
    TestCase
)

# Celery exception.
from celery.exceptions import (
    MaxRetriesExceededError
)

# User model.
from apps.accounts.models import (
    User
)

# Wallet model.
from apps.wallets.models import (
    Wallet
)

# Transaction model.
from apps.transactions.models import (
    Transaction
)

# Audit log.
from apps.audit.models import (
    AuditLog
)

# Task under test.
from apps.transactions.tasks import (
    process_transaction
)


class ProcessTransactionTaskTests(
    TestCase
):

    def setUp(self):
        """
        Build fixture data.
        """

        # Sender.
        self.sender = (
            User.objects.create_user(
                email="sender@test.com",
                username="sender",
                password="Password123!"
            )
        )

        # Receiver.
        self.receiver = (
            User.objects.create_user(
                email="receiver@test.com",
                username="receiver",
                password="Password123!"
            )
        )

        # Sender wallet.
        self.sender_wallet = (
            Wallet.objects.create(
                user=self.sender,
                balance=
                Decimal("1000.00")
            )
        )

        # Receiver wallet.
        self.receiver_wallet = (
            Wallet.objects.create(
                user=self.receiver,
                balance=
                Decimal("100.00")
            )
        )

        # Test transaction.
        self.transaction = (
            Transaction.objects.create(

                sender=
                self.sender,

                receiver=
                self.receiver,

                amount=
                Decimal("100.00")
            )
        )

    @patch(
        "apps.transactions.tasks.transfer_funds"
    )
    def test_successful_transfer(
        self,
        mock_provider
    ):
        """
        Money should move
        between wallets.
        """

        mock_provider.return_value.success = (
            True
        )

        mock_provider.return_value.reference = (
            "PAY-123"
        )

        process_transaction.run(
            self.transaction.id
        )

        self.transaction.refresh_from_db()

        self.sender_wallet.refresh_from_db()

        self.receiver_wallet.refresh_from_db()

        self.assertEqual(

            self.transaction.status,

            Transaction.Status.SUCCESS
        )

        self.assertEqual(

            self.sender_wallet.balance,

            Decimal("900.00")
        )

        self.assertEqual(

            self.receiver_wallet.balance,

            Decimal("200.00")
        )

    @patch(
        "apps.transactions.tasks.transfer_funds"
    )
    @patch(
        "apps.transactions.tasks.process_transaction.retry"
    )
    def test_provider_failure_creates_retry(
        self,
        mock_retry,
        mock_provider
    ):
        """
        Provider failure should
        trigger retry scheduling.
        """

        mock_provider.return_value.success = (
            False
        )

        mock_provider.return_value.message = (
            "Provider unavailable"
        )

        mock_retry.side_effect = (
            RuntimeError(
                "Retry scheduled"
            )
        )

        with self.assertRaises(
            RuntimeError
        ):
            process_transaction.run(
                self.transaction.id
            )

        self.transaction.refresh_from_db()

        self.assertEqual(

            self.transaction.status,

            Transaction.Status.RETRYING
        )

        self.assertEqual(

            self.transaction.retry_count,

            1
        )

    @patch(
        "apps.transactions.tasks.transfer_funds"
    )
    @patch(
        "apps.transactions.tasks.process_transaction.retry"
    )
    def test_retry_creates_audit_record(
        self,
        mock_retry,
        mock_provider
    ):
        """
        Retry should be logged.
        """

        mock_provider.return_value.success = (
            False
        )

        mock_provider.return_value.message = (
            "Provider unavailable"
        )

        mock_retry.side_effect = (
            RuntimeError(
                "Retry scheduled"
            )
        )

        try:

            process_transaction.run(
                self.transaction.id
            )

        except RuntimeError:
            pass

        self.assertTrue(

            AuditLog.objects.filter(
                event_type=
                "TRANSACTION_RETRY"
            ).exists()
        )

    @patch(
        "apps.transactions.tasks.transfer_funds"
    )
    @patch(
        "apps.transactions.tasks.mark_transaction_failed"
    )
    @patch(
        "apps.transactions.tasks.process_transaction.retry"
    )
    def test_max_retries_marks_failed(
        self,
        mock_retry,
        mock_mark_failed,
        mock_provider
    ):
        """
        Permanent failures should
        enter manual-review workflow.
        """

        mock_provider.return_value.success = (
            False
        )

        mock_provider.return_value.message = (
            "Provider unavailable"
        )

        mock_retry.side_effect = (
            MaxRetriesExceededError()
        )

        process_transaction.run(
            self.transaction.id
        )

        mock_mark_failed.assert_called_once()

    @patch(
        "apps.transactions.tasks.transfer_funds"
    )
    def test_success_creates_audit_log(
        self,
        mock_provider
    ):
        """
        Success path should
        create audit event.
        """

        mock_provider.return_value.success = (
            True
        )

        mock_provider.return_value.reference = (
            "PAY-888"
        )

        process_transaction.run(
            self.transaction.id
        )

        self.assertTrue(

            AuditLog.objects.filter(
                event_type=
                "TRANSACTION_SUCCESS"
            ).exists()
        )