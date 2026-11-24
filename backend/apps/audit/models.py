from django.db import models


class AuditLog(models.Model):
    """
    Every important business event
    is stored here.

    In real fintech systems,
    audit trails are mandatory.

    Examples:

    User Registered

    Password Changed

    Transfer Created

    Transfer Failed

    Wallet Credited

    Wallet Debited
    """

    # Event identifier
    event_type = models.CharField(
        max_length=100
    )

    # Human-readable description
    description = models.TextField()

    # Dynamic event data
    metadata = models.JSONField(
        default=dict
    )

    # Creation timestamp
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.event_type} "
            f"{self.created_at}"
        )