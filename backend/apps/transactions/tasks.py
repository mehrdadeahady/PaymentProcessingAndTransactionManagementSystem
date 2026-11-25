# Celery task decorator.
from celery import shared_task

# Retry exception.
from celery.exceptions import (
    MaxRetriesExceededError
)

# Database transactions.
from django.db import transaction

# Audit logging.
from apps.audit.models import (
    AuditLog
)

# Wallets.
from apps.wallets.models import (
    Wallet
)

# Transaction model.
from .models import Transaction

# Provider abstraction.
from .provider import (
    transfer_funds
)

# Services.
from .services import (

    get_transaction_by_id,

    mark_transaction_failed,

    mark_transaction_success
)


@shared_task(
    bind=True,
    max_retries=5
)
def process_transaction(
    self,
    transaction_id
):
    """
    Process transaction.
    """

    tx = get_transaction_by_id(
        transaction_id
    )

    try:

        tx.status = (
            Transaction.Status.PROCESSING
        )

        tx.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        provider_response = (
            transfer_funds(

                sender_id=
                tx.sender.id,

                receiver_id=
                tx.receiver.id,

                amount=
                tx.amount
            )
        )

        if not provider_response.success:

            raise RuntimeError(
                provider_response.message
            )

        with transaction.atomic():

            sender_wallet = (
                Wallet.objects
                .select_for_update()
                .get(
                    user=tx.sender
                )
            )

            receiver_wallet = (
                Wallet.objects
                .select_for_update()
                .get(
                    user=tx.receiver
                )
            )

            sender_wallet.balance -= (
                tx.amount
            )

            receiver_wallet.balance += (
                tx.amount
            )

            sender_wallet.save()

            receiver_wallet.save()

        mark_transaction_success(

            transaction_id=
            tx.id,

            provider_reference=
            provider_response.reference
        )

        return True

    except MaxRetriesExceededError:

        mark_transaction_failed(

            transaction_id=tx.id,

            reason="Max retries exceeded"
        )

        return False

    except Exception as exc:

        tx.refresh_from_db()

        tx.retry_count = (
            self.request.retries + 1
        )

        tx.status = (
            Transaction.Status.RETRYING
        )

        tx.save(
            update_fields=[
                "retry_count",
                "status",
                "updated_at"
            ]
        )

        AuditLog.objects.create(

            event_type=
            "TRANSACTION_RETRY",

            description=
            f"Transaction "
            f"{tx.id} "
            f"retry "
            f"{tx.retry_count}",

            metadata={
                "error":
                str(exc)
            }
        )

        delay_seconds = (
            2 **
            (
                self.request.retries
                + 1
            )
        )

        try:

            self.retry(

                exc=exc,

                countdown=
                delay_seconds
            )

        except MaxRetriesExceededError:

            mark_transaction_failed(

                transaction_id=tx.id,

                reason=str(exc)
            )

            return False