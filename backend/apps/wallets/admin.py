from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "balance",
        "updated_at",
    )

    search_fields = (
        "user__email",
    )

    ordering = (
        "-updated_at",
    )