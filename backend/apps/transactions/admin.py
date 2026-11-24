# Django admin module.
from django.contrib import admin

# Transaction model.
from .models import Transaction


# Register Transaction model
# in Django admin.
@admin.register(Transaction)
class TransactionAdmin(
    admin.ModelAdmin
):
    """
    Admin configuration
    for transactions.
    """

    # Visible columns.
    list_display = (

        "id",

        "sender",

        "receiver",

        "amount",

        "status",

        "retry_count",

        "manual_review_required",

        "created_at",
    )

    # Search fields.
    search_fields = (

        "sender__email",

        "receiver__email",
    )

    # Available admin filters.
    list_filter = (

        "status",

        "manual_review_required",

        "created_at",
    )

    # Sort newest first.
    ordering = (
        "-created_at",
    )

    # Prevent modification.
    readonly_fields = (

        "idempotency_key",

        "created_at",

        "updated_at",
    )