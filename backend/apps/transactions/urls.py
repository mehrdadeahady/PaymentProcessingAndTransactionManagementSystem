# URL routing.
from django.urls import path

# API views.
from .views import (

    TransferAPIView,

    TransactionListAPIView,

    TransactionDetailAPIView
)


urlpatterns = [

    # Transaction history.
    path(

        "",

        TransactionListAPIView
        .as_view(),

        name=
        "transaction-list"
    ),

    # Transaction details.
    path(

        "<int:transaction_id>/",

        TransactionDetailAPIView
        .as_view(),

        name=
        "transaction-detail"
    ),

    # Create transfer.
    path(

        "transfer/",

        TransferAPIView
        .as_view(),

        name=
        "transfer"
    ),
]