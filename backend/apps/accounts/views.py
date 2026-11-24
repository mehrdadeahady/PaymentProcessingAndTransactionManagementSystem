from rest_framework import status

from rest_framework.response import Response

from rest_framework.views import APIView

from apps.wallets.models import Wallet

from .serializers import (
    UserRegistrationSerializer
)


class RegisterAPIView(APIView):

    """
    Create user account
    and user wallet.
    """

    authentication_classes = []

    permission_classes = []

    def post(self, request):

        serializer = (
            UserRegistrationSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        # Create wallet automatically
        Wallet.objects.create(
            user=user
        )

        return Response(
            {
                "message":
                "User created successfully"
            },
            status=status.HTTP_201_CREATED
        )