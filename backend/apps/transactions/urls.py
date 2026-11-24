from django.urls import path

from .views import TransferAPIView

urlpatterns = [

    # Money transfer endpoint.
    path(
        "transfer/",
        TransferAPIView.as_view(),
        name="transfer"
    )
]