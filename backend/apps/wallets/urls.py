# URL helpers.
from django.urls import path

# Wallet endpoints.
from .views import (
    CurrentWalletAPIView
)


urlpatterns = [

    # Current user's wallet.
    path(

        "me/",

        CurrentWalletAPIView.as_view(),

        name="current-wallet"
    ),
]