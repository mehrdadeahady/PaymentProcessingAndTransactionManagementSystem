# Django's built-in abstract user model.
#
# We extend it because fintech systems almost
# always require custom authentication logic.
from django.contrib.auth.models import AbstractUser

# Django ORM base classes.
from django.db import models


class User(AbstractUser):
    """
    Custom User model.

    Why not use Django's default User?

    FinTech systems usually need:

    - custom fields
    - KYC information
    - verification status
    - customer risk scores
    - government IDs
    """

    # Email should be unique because
    # we want users to login with email.
    email = models.EmailField(
        unique=True
    )

    # Instead of username,
    # authentication uses email.
    USERNAME_FIELD = "email"

    # Required when creating superusers.
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email