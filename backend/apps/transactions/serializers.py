# DRF serializers.
from rest_framework import (
    serializers
)

# Models.
from .models import Transaction


class CreateTransactionSerializer(
    serializers.Serializer
):
    """
    Transfer request.
    """

    receiver_id = (
        serializers.IntegerField()
    )

    amount = (
        serializers.DecimalField(

            max_digits=15,

            decimal_places=2
        )
    )


class TransactionSerializer(
    serializers.ModelSerializer
):
    """
    Transaction response.
    """

    class Meta:

        model = Transaction

        fields = (

            "id",

            "sender",

            "receiver",

            "amount",

            "status",

            "retry_count",

            "provider_reference",

            "manual_review_required",

            "created_at",

            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )