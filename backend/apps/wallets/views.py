# DRF permissions.
from rest_framework.permissions import (
    IsAuthenticated
)

# DRF response.
from rest_framework.response import (
    Response
)

# Base API view.
from rest_framework.views import (
    APIView
)

# Shortcuts.
from django.shortcuts import (
    get_object_or_404
)

# Wallet model.
from .models import Wallet

# Serializer.
from .serializers import (
    WalletSerializer
)


class CurrentWalletAPIView(
    APIView
):
    """
    Current user wallet.
    """

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        wallet = (
            get_object_or_404(

                Wallet,

                user=request.user
            )
        )

        serializer = (
            WalletSerializer(
                wallet
            )
        )

        return Response(
            serializer.data
        )