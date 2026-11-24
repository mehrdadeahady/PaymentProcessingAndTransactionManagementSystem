"""
Mock Payment Provider

This module simulates an external payment provider.

Examples of real providers:

- Stripe
- PayPal
- Wise
- Adyen
- Banking APIs

Purpose:

1. Test retry handling
2. Test Celery workers
3. Test audit logging
4. Test failure scenarios
5. Demonstrate fintech architecture

In production this file would make
real HTTP requests to payment services.
"""

# Generate random outcomes.
import random

# Generate unique provider references.
import uuid

# Timestamp generation.
from datetime import datetime


class ProviderResponse:
    """
    Standard provider response.

    Simulates what Stripe, Wise,
    or banking APIs typically return.
    """

    def __init__(
        self,
        success,
        reference,
        message,
    ):
        """
        success:
            Was payment successful?

        reference:
            External provider reference.

        message:
            Human-readable response.
        """

        self.success = success

        self.reference = reference

        self.message = message


def generate_provider_reference():
    """
    Generate unique transaction reference.

    Example:

    PAY-20261123-ABC12345
    """

    # Current UTC date.
    date_part = (
        datetime.utcnow()
        .strftime("%Y%m%d")
    )

    # Random unique value.
    random_part = (
        str(uuid.uuid4())
        .replace("-", "")
        [:8]
        .upper()
    )

    # Final reference.
    return (
        f"PAY-"
        f"{date_part}-"
        f"{random_part}"
    )


def simulate_provider():
    """
    Simulate payment provider behavior.

    Returns:
        True -> Success

        False -> Temporary failure

    Success rate:
        75%

    Failure rate:
        25%

    Used to test:

    - retries
    - exponential backoff
    - monitoring
    - alerting
    """

    return random.choice(
        [
            True,
            True,
            True,
            False,
        ]
    )


def transfer_funds(
    sender_id,
    receiver_id,
    amount,
):
    """
    Simulate money transfer.

    Real implementation might:

    1. Build API request
    2. Sign request
    3. Send HTTPS request
    4. Parse response
    5. Return provider data

    Parameters:

    sender_id:
        Sender identifier

    receiver_id:
        Receiver identifier

    amount:
        Amount to transfer
    """

    # Simulate provider result.
    success = (
        simulate_provider()
    )

    # Generate provider transaction ID.
    provider_reference = (
        generate_provider_reference()
    )

    # Success path.
    if success:

        return ProviderResponse(

            success=True,

            reference=
            provider_reference,

            message=
            "Transfer completed"
        )

    # Failure path.
    return ProviderResponse(

        success=False,

        reference=
        provider_reference,

        message=
        "Provider temporarily unavailable"
    )


def health_check():
    """
    Simulate provider health endpoint.

    Real providers usually expose:

    /health

    /status

    Returns provider availability.
    """

    return {

        "provider": "MockPaymentProvider",

        "status": "healthy",

        "timestamp":
        datetime.utcnow().isoformat(),
    }