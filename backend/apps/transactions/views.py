# UUID support.
import uuid

# Django helpers.
from django.shortcuts import (
    get_object_or_404
)

# DRF.
from rest_framework import status

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import (
    Response
)

from rest_framework.views import (
    APIView
)

# Models.
from apps.accounts.models import (
    User
)

# Services.
from .services import (
    create_transaction
)

# Tasks.
from .tasks import (
    process_transaction
)

# Transaction model.
from .models import Transaction

# Serializers.
from .serializers import (

    CreateTransactionSerializer,

    TransactionSerializer
)


class TransferAPIView(
    APIView
):
    """
    Transfer endpoint.
    """

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        serializer = (
            CreateTransactionSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        receiver = (
            get_object_or_404(

                User,

                id=serializer
                .validated_data[
                    "receiver_id"
                ]
            )
        )

        amount = (
            serializer
            .validated_data[
                "amount"
            ]
        )

        idempotency_key = (
            request.headers.get(
                "Idempotency-Key",
                str(uuid.uuid4())
            )
        )

        tx = create_transaction(

            sender=request.user,

            receiver=receiver,

            amount=amount,

            idempotency_key=
            idempotency_key
        )

        process_transaction.delay(
            tx.id
        )

        return Response(

            {

                "transaction_id":
                tx.id,

                "status":
                tx.status
            },

            status=
            status.HTTP_201_CREATED
        )


class TransactionListAPIView(
    APIView
):
    """
    List user transactions.
    """

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        transactions = (

            Transaction.objects.filter(
                sender=request.user
            )

            |

            Transaction.objects.filter(
                receiver=request.user
            )

        ).distinct().order_by(
            "-created_at"
        )

        serializer = (
            TransactionSerializer(

                transactions,

                many=True
            )
        )

        return Response(
            serializer.data
        )


class TransactionDetailAPIView(
    APIView
):
    """
    Transaction detail.
    """

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        transaction_id
    ):

        transaction = (
            get_object_or_404(

                Transaction,

                id=transaction_id
            )
        )

        if (
            transaction.sender
            != request.user
            and
            transaction.receiver
            != request.user
        ):

            return Response(

                {
                    "detail":
                    "Not found."
                },

                status=404
            )

        serializer = (
            TransactionSerializer(
                transaction
            )
        )

        return Response(
            serializer.data
        )