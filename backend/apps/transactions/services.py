"""
Transaction Service Layer

Purpose:

Keep business logic outside views.

Views should:

- Receive requests
- Validate data
- Return responses

Services should:

- Execute business rules
- Validate balances
- Prevent duplicates
- Create transactions
- Write audit logs

This pattern is commonly used in
production Django applications.
"""

# Decimal is required for money.
#
# Never use float for currency.
from decimal import Decimal

# Database transaction support.
#
# Allows atomic operations.
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


class TransactionException(
    Exception
):
    """
    Base transaction exception.
    """
    pass


class InsufficientFundsException(
    TransactionException
):
    """
    Raised when user balance
    is lower than requested amount.
    """
    pass


class InvalidTransferException(
    TransactionException
):
    """
    Raised when business rules
    are violated.
    """
    pass


def validate_transfer(
    sender,
    receiver,
    amount,
):
    """
    Validate transfer request.

    Rules:

    - Sender cannot send to self
    - Amount must be positive
    - Amount must be greater than zero
    """

    # Prevent self-transfer.
    if sender.id == receiver.id:

        raise InvalidTransferException(
            "You cannot transfer money "
            "to yourself."
        )

    # Prevent negative amounts.
    if amount <= Decimal("0.00"):

        raise InvalidTransferException(
            "Amount must be greater than zero."
        )


def get_wallet_balance(
    user,
):
    """
    Return current wallet balance.
    """

    wallet = Wallet.objects.get(
        user=user
    )

    return wallet.balance


def validate_sufficient_balance(
    sender,
    amount,
):
    """
    Ensure sender has enough money.

    Note:

    Actual debit occurs later
    inside Celery processing.

    We still validate early
    to avoid obviously invalid
    requests.
    """

    wallet = Wallet.objects.get(
        user=sender
    )

    if wallet.balance < amount:

        raise InsufficientFundsException(
            "Insufficient funds."
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

    Protected by:

    - Database transaction
    - Idempotency key
    - Business validations

    Returns transaction record.
    """

    # Validate request.
    validate_transfer(
        sender,
        receiver,
        amount
    )

    # Validate balance.
    validate_sufficient_balance(
        sender,
        amount
    )

    # Check for duplicate request.
    existing_transaction = (
        Transaction.objects.filter(
            idempotency_key=idempotency_key
        ).first()
    )

    # Return existing transaction
    # if already processed.
    if existing_transaction:

        return existing_transaction

    # Create new transaction.
    tx = Transaction.objects.create(

        sender=sender,

        receiver=receiver,

        amount=amount,

        idempotency_key=
        idempotency_key,

        status=
        Transaction.Status.PENDING,
    )

    # Audit creation.
    AuditLog.objects.create(

        event_type=
        "TRANSACTION_CREATED",

        description=
        f"Transaction "
        f"{tx.id} "
        f"created",

        metadata={

            "transaction_id":
            tx.id,

            "sender":
            sender.id,

            "receiver":
            receiver.id,

            "amount":
            str(amount),

            "idempotency_key":
            str(idempotency_key),
        }
    )

    return tx


def get_transaction_by_id(
    transaction_id,
):
    """
    Retrieve transaction.
    """

    return Transaction.objects.get(
        id=transaction_id
    )


def get_user_transactions(
    user,
):
    """
    Return user transactions.

    Includes:

    - Sent transfers
    - Received transfers
    """

    return (
        Transaction.objects
        .filter(
            sender=user
        )
        .union(
            Transaction.objects.filter(
                receiver=user
            )
        )
        .order_by(
            "-created_at"
        )
    )


def mark_transaction_failed(
    transaction_id,
    reason,
):
    """
    Mark transaction failed.

    Used when business process
    encounters unrecoverable failure.
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
    provider_reference,
):
    """
    Mark transaction successful.

    Store provider transaction id.
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