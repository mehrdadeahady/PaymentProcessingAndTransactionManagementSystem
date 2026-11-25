# DRF response helpers.
from rest_framework import status

# Permissions.
from rest_framework.permissions import (
    AllowAny
)

# API responses.
from rest_framework.response import (
    Response
)

# Base view.
from rest_framework.views import (
    APIView
)

# Wallet model.
from apps.wallets.models import (
    Wallet
)

# Serializers.
from .serializers import (

    UserRegistrationSerializer,

    EmailTokenObtainSerializer
)


class RegisterAPIView(
    APIView
):
    """
    Register user.
    """

    permission_classes = [
        AllowAny
    ]

    def post(
        self,
        request
    ):

        serializer = (
            UserRegistrationSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        # Create wallet.
        Wallet.objects.get_or_create(
            user=user
        )

        return Response(

            {
                "message":
                "User created successfully"
            },

            status=
            status.HTTP_201_CREATED
        )


class EmailTokenObtainAPIView(
    APIView
):
    """
    Email login endpoint.
    """

    permission_classes = [
        AllowAny
    ]

    def post(
        self,
        request
    ):

        serializer = (
            EmailTokenObtainSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        return Response(
            serializer.validated_data
        )