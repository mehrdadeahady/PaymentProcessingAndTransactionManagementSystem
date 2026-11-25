# Authentication.
from django.contrib.auth import (
    authenticate
)

# DRF.
from rest_framework import (
    serializers
)

# JWT.
from rest_framework_simplejwt.tokens import (
    RefreshToken
)

# User model.
from .models import User


class UserRegistrationSerializer(
    serializers.ModelSerializer
):

    password = (
        serializers.CharField(

            write_only=True,

            min_length=8
        )
    )

    class Meta:

        model = User

        fields = (

            "email",

            "username",

            "password"
        )

    def create(
        self,
        validated_data
    ):

        return User.objects.create_user(

            email=
            validated_data["email"],

            username=
            validated_data["username"],

            password=
            validated_data["password"]
        )


class EmailTokenObtainSerializer(
    serializers.Serializer
):

    email = (
        serializers.EmailField()
    )

    password = (
        serializers.CharField(
            write_only=True
        )
    )

    def validate(
        self,
        attrs
    ):

        email = attrs.get(
            "email"
        )

        password = attrs.get(
            "password"
        )

        user = authenticate(

            username=email,

            password=password
        )

        if not user:

            raise (
                serializers.ValidationError(
                    "Invalid credentials."
                )
            )

        refresh = (
            RefreshToken.for_user(
                user
            )
        )

        return {

            "access":

            str(
                refresh.access_token
            ),

            "refresh":

            str(refresh)
        }