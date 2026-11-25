# DRF serializers.
from rest_framework import (
    serializers
)

# Wallet model.
from .models import Wallet


class WalletSerializer(
    serializers.ModelSerializer
):
    """
    Wallet serializer.
    """

    class Meta:

        model = Wallet

        fields = (

            "id",

            "user",

            "balance",

            "updated_at"
        )

        read_only_fields = (

            "id",

            "updated_at"
        )