from django.apps import AppConfig


class AccountsConfig(AppConfig):

    # Default primary key type
    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    # Django app name
    name = "apps.accounts"

    # Human-readable name in admin panel
    verbose_name = (
        "Accounts Management"
    )