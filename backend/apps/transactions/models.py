# UUID support.
import uuid

# Django ORM.
from django.db import models

# User model.
from apps.accounts.models import (
    User
)


class Transaction(
    models.Model
):

    class Status(
        models.TextChoices
    ):

        PENDING = (
            "PENDING"
        )

        PROCESSING = (
            "PROCESSING"
        )

        SUCCESS = (
            "SUCCESS"
        )

        FAILED = (
            "FAILED"
        )

        RETRYING = (
            "RETRYING"
        )

    sender = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name=
        "sent_transactions"
    )

    receiver = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name=
        "received_transactions"
    )

    amount = models.DecimalField(

        max_digits=15,

        decimal_places=2
    )

    status = models.CharField(

        max_length=20,

        choices=Status.choices,

        default=Status.PENDING
    )

    retry_count = (
        models.IntegerField(
            default=0
        )
    )

    idempotency_key = (
        models.UUIDField(

            default=uuid.uuid4,

            unique=True
        )
    )

    provider_reference = (
        models.CharField(

            max_length=100,

            blank=True,

            null=True
        )
    )

    manual_review_required = (
        models.BooleanField(
            default=False
        )
    )

    created_at = (
        models.DateTimeField(
            auto_now_add=True
        )
    )

    updated_at = (
        models.DateTimeField(
            auto_now=True
        )
    )

    def __str__(self):

        return (

            f"Transaction "

            f"{self.id} "

            f"({self.status})"
        )