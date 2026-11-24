# Generates UUID values.
import uuid

# Django model lookup helper.
from django.shortcuts import get_object_or_404

# DRF response utilities.
from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.views import APIView

# User model.
from apps.accounts.models import User

# Business logic.
from .services import create_transaction

# Async processor.
from .tasks import process_transaction

# Validators.
from .serializers import (
    CreateTransactionSerializer
)


class TransferAPIView(APIView):
    """
    Creates transfer.

    POST

    /api/transactions/transfer/
    """

    # Only authenticated users.
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        # Validate payload.
        serializer = (
            CreateTransactionSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        # Find receiver.
        receiver = get_object_or_404(
            User,
            id=serializer.validated_data[
                "receiver_id"
            ]
        )

        # Get amount.
        amount = serializer.validated_data[
            "amount"
        ]

        # Read idempotency header.
        #
        # Prevents duplicate requests.
        idempotency_key = (
            request.headers.get(
                "Idempotency-Key",
                str(uuid.uuid4())
            )
        )

        # Create transaction.
        tx = create_transaction(
            sender=request.user,
            receiver=receiver,
            amount=amount,
            idempotency_key=idempotency_key
        )

        # Background processing.
        #
        # API returns immediately
        # without waiting.
        process_transaction.delay(
            tx.id
        )

        return Response(
            {
                "transaction_id": tx.id,
                "status": tx.status
            },
            status=status.HTTP_201_CREATED
        )