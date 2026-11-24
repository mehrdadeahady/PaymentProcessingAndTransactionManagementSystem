from rest_framework import serializers

from .models import Transaction


class CreateTransactionSerializer(
    serializers.Serializer
):
    """
    Input validation.

    Incoming request:

    {
        "receiver_id": 2,
        "amount": "100.00"
    }
    """

    # Receiver user id.
    receiver_id = serializers.IntegerField()

    # Transfer amount.
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class TransactionSerializer(
    serializers.ModelSerializer
):
    """
    Converts Transaction model
    into API response.
    """

    class Meta:

        model = Transaction

        fields = "__all__"