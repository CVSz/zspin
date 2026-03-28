from __future__ import annotations

import os

import stripe

stripe.api_key = os.getenv("STRIPE_KEY", "")


def charge(customer_id: str, amount: float) -> stripe.PaymentIntent:
    return stripe.PaymentIntent.create(
        amount=int(amount * 100),
        currency="usd",
        customer=customer_id,
    )
