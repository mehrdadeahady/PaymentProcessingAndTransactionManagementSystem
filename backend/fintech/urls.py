from django.contrib import admin

from django.urls import (
    include,
    path
)

# JWT authentication endpoints.
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # Django admin.
    path(
        "admin/",
        admin.site.urls
    ),

    # Accounts APIs.
    path(
        "api/accounts/",
        include(
            "apps.accounts.urls"
        )
    ),

    # Authentication.
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    # Transaction APIs.
    path(
        "api/transactions/",
        include(
            "apps.transactions.urls"
        )
    ),
]