"""Stripe billing integration for example checkout flow."""

from __future__ import annotations

import os

import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY", "sk_test_xxx")


def create_checkout() -> str:
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "zspin Pro"},
                    "unit_amount": 4900,
                    "recurring": {"interval": "month"},
                },
                "quantity": 1,
            }
        ],
        mode="subscription",
        success_url=os.getenv("STRIPE_SUCCESS_URL", "http://localhost:3000"),
        cancel_url=os.getenv("STRIPE_CANCEL_URL", "http://localhost:3000"),
    )
    return str(session.url)
