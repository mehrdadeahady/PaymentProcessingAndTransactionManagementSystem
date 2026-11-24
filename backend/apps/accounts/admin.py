from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    # Columns shown in admin list
    list_display = (
        "id",
        "email",
        "username",
        "is_active",
        "date_joined",
    )

    # Search box
    search_fields = (
        "email",
        "username",
    )

    # Filters right-side
    list_filter = (
        "is_active",
        "is_staff",
        "date_joined",
    )