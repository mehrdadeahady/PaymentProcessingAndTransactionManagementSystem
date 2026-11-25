# Decimal support.
from decimal import Decimal

# Django settings.
from django.conf import settings

# Django ORM.
from django.db import models


class Wallet(
    models.Model
):
    """
    User wallet.
    """

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="wallet"
    )

    balance = models.DecimalField(

        max_digits=15,

        decimal_places=2,

        default=Decimal("0.00")
    )

    updated_at = (
        models.DateTimeField(
            auto_now=True
        )
    )

    def __str__(self):

        return (

            f"{self.user.email} "

            f"({self.balance})"
        )