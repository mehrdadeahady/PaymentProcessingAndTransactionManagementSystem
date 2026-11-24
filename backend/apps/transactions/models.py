# Generate unique UUID values.
#
# Used for idempotency keys which prevent
# duplicate transaction execution.
import uuid

# Django ORM base classes.
from django.db import models

# User model.
from apps.accounts.models import User


class Transaction(models.Model):
    """
    Represents a money transfer.

    Example:

    User A
        ↓
     $100
        ↓
    User B
    """

    class Status(models.TextChoices):
        """
        Allowed transaction states.
        """

        # Transaction created.
        PENDING = "PENDING"

        # Worker is processing.
        PROCESSING = "PROCESSING"

        # Transaction completed.
        SUCCESS = "SUCCESS"

        # Transaction exhausted retries.
        FAILED = "FAILED"

        # Waiting for another retry.
        RETRYING = "RETRYING"

    # Sender account.
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_transactions"
    )

    # Receiver account.
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_transactions"
    )

    # Transfer amount.
    #
    # Decimal must always be used
    # for financial calculations.
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    # Current status.
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    # Number of retry attempts.
    retry_count = models.IntegerField(
        default=0
    )

    # Unique protection key.
    #
    # Prevents duplicate transfers.
    #
    # Example:
    #
    # User clicks Send twice.
    #
    # Same idempotency key
    # returns same transaction.
    idempotency_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    # External provider reference.
    #
    # Example:
    #
    # Stripe payment id
    # Bank transaction id
    provider_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # Flag requiring operations 