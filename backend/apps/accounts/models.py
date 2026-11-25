# Django user base model.
from django.contrib.auth.models import (
    AbstractUser
)

# Django ORM.
from django.db import models


class User(
    AbstractUser
):
    """
    Custom user model.

    Authentication is based
    on email address.
    """

    # Unique email.
    email = models.EmailField(
        unique=True
    )

    # Use email for login.
    USERNAME_FIELD = "email"

    # Required for admin user.
    REQUIRED_FIELDS = [
        "username"
    ]

    def __str__(self):

        return self.email