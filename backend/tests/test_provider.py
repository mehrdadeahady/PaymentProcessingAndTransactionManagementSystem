"""
Provider tests.
"""

from django.test import TestCase

from apps.transactions.provider import (

    generate_provider_reference,

    transfer_funds,

    health_check,
)


class ProviderTests(
    TestCase
):

    def test_reference_generated(self):

        reference = (
            generate_provider_reference()
        )

        self.assertTrue(
            reference.startswith("PAY-")
        )

    def test_health_check(self):

        result = health_check()

        self.assertEqual(
            result["status"],
            "healthy"
        )

    def test_transfer_response(self):

        response = transfer_funds(

            sender_id=1,

            receiver_id=2,

            amount=100,
        )

        self.assertIsNotNone(
            response.reference
        )