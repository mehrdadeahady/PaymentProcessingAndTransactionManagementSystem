# Decimal money support.
from decimal import Decimal

# Database transactions.
from django.db import transaction

# Auditing.
from apps.audit.models import (
    AuditLog
)

# Wallet model.
from apps.wallets.models import (
    Wallet
)

# Transaction model.
from .models import Transaction


class TransactionException(
    Exception
):
    pass


class InsufficientFundsException(
    TransactionException
):
    pass


class InvalidTransferException(
    TransactionException
):
    pass


def validate_transfer(
    sender,
    receiver,
    amount,
):
    """
    Validate transfer.
    """

    if sender.id == receiver.id:

        raise (
            InvalidTransferException(
                "Cannot transfer to yourself."
            )
        )

    if amount <= Decimal("0.00"):

        raise (
            InvalidTransferException(
                "Amount must be greater than zero."
            )
        )


def validate_sufficient_balance(
    sender,
    amount
):
    """
    Validate balance.
    """

    wallet = Wallet.objects.get(
        user=sender
    )

    if wallet.balance < amount:

        raise (
            InsufficientFundsException(
                "Insufficient funds."
            )
        )


@transaction.atomic
def create_transaction(
    sender,
    receiver,
    amount,
    idempotency_key,
):
    """
    Create transaction.
    """

    validate_transfer(

        sender,
        receiver,
        amount
    )

    validate_sufficient_balance(

        sender,
        amount
    )

    existing = (
        Transaction.objects.filter(
            idempotency_key=
            idempotency_key
        ).first()
    )

    if existing:

        return existing

    tx = Transaction.objects.create(

        sender=sender,

        receiver=receiver,

        amount=amount,

        idempotency_key=
        idempotency_key,

        status=
        Transaction.Status.PENDING
    )

    AuditLog.objects.create(

        event_type=
        "TRANSACTION_CREATED",

        description=
        f"Transaction "
        f"{tx.id} "
        f"created",

        metadata={

            "sender":
            sender.id,

            "receiver":
            receiver.id,

            "amount":
            str(amount),

            "idempotency_key":
            str(idempotency_key)
        }
    )

    return tx


def get_transaction_by_id(
    transaction_id
):
    """
    Get transaction.
    """

    return Transaction.objects.get(
        id=transaction_id
    )


def get_user_transactions(
    user
):
    """
    User transaction history.
    """

    return (

        Transaction.objects.filter(
            sender=user
        )

        |

        Transaction.objects.filter(
            receiver=user
        )

    ).distinct().order_by(
        "-created_at"
    )


def mark_transaction_failed(
    transaction_id,
    reason
):
    """
    Mark failed.
    """

    tx = Transaction.objects.get(
        id=transaction_id
    )

    tx.status = (
        Transaction.Status.FAILED
    )

    tx.manual_review_required = (
        True
    )

    tx.save()

    AuditLog.objects.create(

        event_type=
        "TRANSACTION_FAILED",

        description=
        f"Transaction "
        f"{tx.id} "
        f"failed",

        metadata={
            "reason":
            str(reason)
        }
    )

    return tx


def mark_transaction_success(
    transaction_id,
    provider_reference
):
    """
    Mark successful.
    """

    tx = Transaction.objects.get(
        id=transaction_id
    )

    tx.status = (
        Transaction.Status.SUCCESS
    )

    tx.provider_reference = (
        provider_reference
    )

    tx.save()

    AuditLog.objects.create(

        event_type=
        "TRANSACTION_SUCCESS",

        description=
        f"Transaction "
        f"{tx.id} "
        f"completed",

        metadata={
            "provider_reference":
            provider_reference
        }
    )

    return tx