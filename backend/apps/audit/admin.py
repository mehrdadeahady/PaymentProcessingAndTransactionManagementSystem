from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "event_type",
        "created_at",
    )

    search_fields = (
        "event_type",
        "description",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "metadata",
        "created_at",
    )