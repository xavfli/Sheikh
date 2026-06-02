import base64
import hashlib
import urllib.parse
import urllib.request
from decimal import Decimal

import stripe
from django.conf import settings
from django.urls import reverse

from .models import PaymentTransaction


def absolute_url(path: str) -> str:
    return f"{settings.SITE_URL.rstrip('/')}{path}"


def provider_enabled(provider: str) -> bool:
    checks = {
        PaymentTransaction.Provider.STRIPE: bool(settings.STRIPE_SECRET_KEY),
        PaymentTransaction.Provider.CLICK: bool(
            settings.CLICK_SERVICE_ID and settings.CLICK_MERCHANT_ID and settings.CLICK_SECRET_KEY
        ),
        PaymentTransaction.Provider.PAYME: bool(settings.PAYME_MERCHANT_ID),
    }
    return checks.get(provider, False)


def available_providers():
    return [
        {"key": provider, "label": label, "enabled": provider_enabled(provider)}
        for provider, label in PaymentTransaction.Provider.choices
    ]


def send_telegram_message(text: str) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode(
        {"chat_id": settings.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    ).encode()
    request = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=10):
            return True
    except Exception:
        return False


def notify_purchase(transaction: PaymentTransaction):
    text = (
        f"<b>Yangi buyurtma</b>\n"
        f"Provider: {transaction.get_provider_display()}\n"
        f"Order: {transaction.order_id}\n"
        f"User: {transaction.buyer.username}\n"
        f"Account: {transaction.account.title}\n"
        f"Summa: ${transaction.amount}"
    )
    send_telegram_message(text)


def create_stripe_checkout(transaction: PaymentTransaction):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        mode="payment",
        client_reference_id=transaction.order_id,
        success_url=absolute_url(
            reverse("market:payment_success") + "?provider=stripe&session_id={CHECKOUT_SESSION_ID}"
        ),
        cancel_url=absolute_url(reverse("market:payment_cancel") + f"?order_id={transaction.order_id}"),
        customer_email=transaction.buyer.email or None,
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(Decimal(transaction.amount) * 100),
                    "product_data": {
                        "name": transaction.account.title,
                        "description": transaction.account.short_description,
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={
            "order_id": transaction.order_id,
            "account_id": str(transaction.account_id),
            "buyer_id": str(transaction.buyer_id),
        },
    )
    transaction.provider_reference = session.id
    transaction.payload = {**transaction.payload, "checkout_url": session.url}
    transaction.save(update_fields=["provider_reference", "payload", "updated_at"])
    return session.url


def build_click_url(transaction: PaymentTransaction):
    params = {
        "service_id": settings.CLICK_SERVICE_ID,
        "merchant_id": settings.CLICK_MERCHANT_ID,
        "merchant_user_id": settings.CLICK_MERCHANT_USER_ID,
        "amount": f"{transaction.amount:.2f}",
        "transaction_param": transaction.order_id,
        "return_url": absolute_url(reverse("market:payment_success") + f"?provider=click&order_id={transaction.order_id}"),
    }
    return f"{settings.CLICK_BASE_URL}?{urllib.parse.urlencode(params)}"


def build_payme_url(transaction: PaymentTransaction):
    raw = (
        f"m={settings.PAYME_MERCHANT_ID};"
        f"ac.order_id={transaction.order_id};"
        f"a={int(Decimal(transaction.amount) * 100)};"
        f"l=uz;"
        f"c={absolute_url(reverse('market:payment_success') + f'?provider=payme&order_id={transaction.order_id}')}"
    )
    encoded = base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")
    return f"{settings.PAYME_CHECKOUT_URL}/{encoded}"


def verify_click_prepare_signature(data):
    check = hashlib.md5(
        (
            f"{data.get('click_trans_id', '')}"
            f"{data.get('service_id', '')}"
            f"{settings.CLICK_SECRET_KEY}"
            f"{data.get('merchant_trans_id', '')}"
            f"{data.get('amount', '')}"
            f"{data.get('action', '')}"
            f"{data.get('sign_time', '')}"
        ).encode()
    ).hexdigest()
    return check == data.get("sign_string", "")


def verify_click_complete_signature(data):
    check = hashlib.md5(
        (
            f"{data.get('click_trans_id', '')}"
            f"{data.get('service_id', '')}"
            f"{settings.CLICK_SECRET_KEY}"
            f"{data.get('merchant_trans_id', '')}"
            f"{data.get('merchant_prepare_id', '')}"
            f"{data.get('amount', '')}"
            f"{data.get('action', '')}"
            f"{data.get('sign_time', '')}"
        ).encode()
    ).hexdigest()
    return check == data.get("sign_string", "")


def mark_transaction_paid(transaction: PaymentTransaction, external_id: str = "", payload: dict | None = None):
    purchase = transaction.mark_paid(external_id=external_id, payload=payload)
    notify_purchase(transaction)
    return purchase
