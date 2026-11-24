# Celery task decorator.
from celery import shared_task

# Exception raised when a task has
# exhausted all retry attempts.
from celery.exceptions import (
    MaxRetriesExceededError
)

# Database transaction support.
from django.db import transaction

# Audit logging.
from apps.audit.models import (
    AuditLog
)

# Wallet model.
from apps.wallets.models import (
    Wallet
)

# Transaction model.
from .models import Transaction

# External provider abstraction.
from .provider import transfer_funds

# Service-layer functions.
from .services import (
    get_transaction_by_id,
    mark_transaction_failed,
    mark_transaction_success,
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
    Process financial transaction.

    Retry schedule:

    Retry 1 -> 2 sec

    Retry 2 -> 4 sec

    Retry 3 -> 8 sec

    Retry 4 -> 16 sec

    Retry 5 -> 32 sec
    """

    # Load transaction.
    tx = get_transaction_by_id(
        transaction_id
    )

    try:

        # Mark processing.
        tx.status = (
            Transaction.Status.PROCESSING
        )

        tx.save()

        # Send request to provider.
        provider_response = (
            transfer_funds(

                sender_id=
                tx.sender.id,

                receiver_id=
                tx.receiver.id,

                amount=
                tx.amount,
            )
        )

        # Temporary provider failure.
        if not provider_response.success:

            raise RuntimeError(
                provider_response.message
            )

        # Atomic balance update.
        #
        # Either both wallet updates
        # succeed or both rollback.
        with transaction.atomic():

            # Lock sender wallet.
            sender_wallet = (
                Wallet.objects
                .select_for_update()
                .get(
                    user=tx.sender
                )
            )

            # Lock receiver wallet.
            receiver_wallet = (
                Wallet.objects
                .select_for_update()
                .get(
                    user=tx.receiver
                )
            )

            # Debit sender.
            sender_wallet.balance -= (
                tx.amount
            )

            # Credit receiver.
            receiver_wallet.balance += (
                tx.amount
            )

            sender_wallet.save()

            receiver_wallet.save()

        # Mark successful.
        mark_transaction_success(

            transaction_id=tx.id,

            provider_reference=
            provider_response.reference,
        )

        return True

    except Exception as exc:

        # Update retry state.
        tx.retry_count = (
            self.request.retries + 1
        )

        tx.status = (
            Transaction.Status.RETRYING
        )

        tx.save()

        # Audit retry.
        AuditLog.objects.create(

            event_type=
            "TRANSACTION_RETRY",

            description=
            f"Transaction "
            f"{tx.id} "
            f"retry "
            f"{tx.retry_count}",

            metadata={

                "retry_count":
                tx.retry_count,

                "error":
                str(exc),
            }
        )

        # Calculate exponential backoff.
        delay_seconds = (
            2 **
            (
                self.request.retries
                + 1
            )
        )

        try:

            # Schedule another attempt.
            self.retry(

                exc=exc,

                countdown=
                delay_seconds
            )

        except MaxRetriesExceededError:

            # Permanent failure.
            mark_transaction_failed(

                transaction_id=tx.id,

                reason=str(exc)
            )

            return False
