import base64
import json
import secrets
from datetime import datetime
from decimal import Decimal
from urllib.parse import quote

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import SignUpForm, StyledAuthenticationForm
from .models import Category, GameAccount, PaymentTransaction, Purchase
from .services import (
    available_providers,
    build_click_url,
    build_payme_url,
    create_stripe_checkout,
    mark_transaction_paid,
    provider_enabled,
    verify_click_complete_signature,
    verify_click_prepare_signature,
)
from .telegram_bot import process_update

GAME_SHOWCASES = {
    "pubg-mobile": {
        "label": "PUBG Mobile",
        "icon": "PUBG",
        "accent": "gold",
        "cards": [
            {
                "title": "PUBG MOBILE RANDOM",
                "image": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=700&q=80",
            },
            {
                "title": "Pubg Mobile Satlik Hesap",
                "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=700&q=80",
            },
            {
                "title": "Pubg Sipriz UC Paketleri",
                "image": "https://images.unsplash.com/photo-1486572788966-cfd3df1f5b42?auto=format&fit=crop&w=700&q=80",
            },
        ],
        "catalog_heading": "PUBG Mobile vitrin ilanlari",
    },
    "mobile-legends": {
        "label": "Mobile Legends",
        "icon": "ML",
        "accent": "pink",
        "cards": [
            {
                "title": "Mobile Legends Elmas",
                "image": "https://images.unsplash.com/photo-1560419015-7c427e8ae5ba?auto=format&fit=crop&w=700&q=80",
            },
            {
                "title": "Epic Skinli ML Hesap",
                "image": "https://images.unsplash.com/photo-1511882150382-421056c89033?auto=format&fit=crop&w=700&q=80",
            },
        ],
        "catalog_heading": "Mobile Legends premium katalogi",
    },
    "steam": {
        "label": "Steam",
        "icon": "S",
        "accent": "blue",
        "cards": [
            {
                "title": "Oyun Satin Al",
                "image": "https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?auto=format&fit=crop&w=700&q=80",
            },
            {
                "title": "Steam Wallet + Bundle",
                "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=700&q=80",
            },
        ],
        "catalog_heading": "Steam offer katalogi",
    },
}

STATIC_GAME_CATALOGS = {
    "mobile-legends": [
        {
            "title": "ML ELMAS 5K PACKAGE",
            "image": "https://images.unsplash.com/photo-1560419015-7c427e8ae5ba?auto=format&fit=crop&w=900&q=80",
            "stock": "Stokda Mavcut",
            "platform": "Mobile",
            "region": "Global",
            "category": "Diamond",
            "old_price": "55",
            "price": "39",
            "badge": "5K",
            "action_label": "Buyurtma Berish",
        },
        {
            "title": "MYTHIC SKINLI ML ID",
            "image": "https://images.unsplash.com/photo-1511882150382-421056c89033?auto=format&fit=crop&w=900&q=80",
            "stock": "Stokda Mavcut",
            "platform": "Mobile",
            "region": "Asia",
            "category": "Account",
            "old_price": "129",
            "price": "94",
            "badge": "Mythic",
            "action_label": "Buyurtma Berish",
        },
        {
            "title": "EPIC HERO BUNDLE",
            "image": "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=900&q=80",
            "stock": "Stokda Mavcut",
            "platform": "Mobile",
            "region": "EU",
            "category": "Bundle",
            "old_price": "74",
            "price": "51",
            "badge": "Epic",
            "action_label": "Buyurtma Berish",
        },
        {
            "title": "LEGEND RANK STARTER",
            "image": "https://images.unsplash.com/photo-1542751110-97427bbecf20?auto=format&fit=crop&w=900&q=80",
            "stock": "Stokda Mavcut",
            "platform": "Mobile",
            "region": "TR",
            "category": "Rank Push",
            "old_price": "88",
            "price": "63",
            "badge": "Legend",
            "action_label": "Buyurtma Berish",
        },
    ],
    "steam": [
        {
            "title": "STEAM WALLET 50 USD",
            "image": "https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?auto=format&fit=crop&w=900&q=80",
            "stock": "Instant Delivery",
            "platform": "Steam",
            "region": "Global",
            "category": "Wallet",
            "old_price": "60",
            "price": "50",
            "badge": "Wallet",
            "action_label": "Sotib Olish",
        },
        {
            "title": "AAA GAME BUNDLE",
            "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
            "stock": "Stokda Mavcut",
            "platform": "Steam",
            "region": "EU",
            "category": "Bundle",
            "old_price": "119",
            "price": "84",
            "badge": "AAA",
            "action_label": "Sotib Olish",
        },
        {
            "title": "STEAM ACCOUNT PRIME",
            "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=900&q=80",
            "stock": "Stokda Mavcut",
            "platform": "Steam",
            "region": "US",
            "category": "Account",
            "old_price": "145",
            "price": "110",
            "badge": "Prime",
            "action_label": "Sotib Olish",
        },
        {
            "title": "INDIE MEGA PACK",
            "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=900&q=80",
            "stock": "Instant Delivery",
            "platform": "Steam",
            "region": "Global",
            "category": "Indie",
            "old_price": "43",
            "price": "31",
            "badge": "Indie",
            "action_label": "Sotib Olish",
        },
    ],
}


class MarketLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = StyledAuthenticationForm


class MarketLogoutView(LogoutView):
    next_page = "market:home"


def build_telegram_bot_link(account):
    username = settings.TELEGRAM_BOT_USERNAME.strip().lstrip("@")
    if not username:
        return ""
    message = (
        f"Sotib olmoqchiman:%0A"
        f"Account: {quote(account.title)}%0A"
        f"Narxi: {quote(str(account.price))}$%0A"
        f"Platforma: {quote(account.platform)}%0A"
        f"Region: {quote(account.region)}%0A"
        f"Rank: {quote(account.rank_tier)}"
    )
    return f"https://t.me/{username}?text={message}"


def build_telegram_contact_link(account):
    username = settings.TELEGRAM_CONTACT_USERNAME.strip().lstrip("@")
    if not username:
        return ""
    message = (
        f"Salom, {quote(account.title)} account bo'yicha bog'landim.%0A"
        f"Narxi: {quote(str(account.price))}$"
    )
    return f"https://t.me/{username}?text={message}"


def home(request):
    accounts = GameAccount.objects.select_related("category").prefetch_related("videos").all()
    categories = Category.objects.all()

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    platform = request.GET.get("platform", "").strip()
    rank = request.GET.get("rank", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    active_game = request.GET.get("game", "pubg-mobile").strip()
    if active_game not in GAME_SHOWCASES:
        active_game = "pubg-mobile"

    if query:
        accounts = accounts.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(rank_tier__icontains=query)
        )
    if category_slug:
        accounts = accounts.filter(category__slug=category_slug)
    if platform:
        accounts = accounts.filter(platform__iexact=platform)
    if rank:
        accounts = accounts.filter(rank_tier__icontains=rank)
    if min_price:
        accounts = accounts.filter(price__gte=min_price)
    if max_price:
        accounts = accounts.filter(price__lte=max_price)

    featured_accounts = GameAccount.objects.select_related("category").filter(is_featured=True)[:3]
    active_showcase = GAME_SHOWCASES[active_game]
    active_catalog_items = STATIC_GAME_CATALOGS.get(active_game, [])
    stats = {
        "accounts": GameAccount.objects.count(),
        "featured": GameAccount.objects.filter(is_featured=True).count(),
        "sold": Purchase.objects.aggregate(total=Count("id"))["total"] or 0,
        "platforms": GameAccount.objects.values("platform").distinct().count(),
    }
    return render(
        request,
        "market/home.html",
        {
            "accounts": accounts,
            "categories": categories,
            "featured_accounts": featured_accounts,
            "stats": stats,
            "active_game": active_game,
            "game_navigation": GAME_SHOWCASES,
            "game_catalogs": STATIC_GAME_CATALOGS,
            "active_showcase": active_showcase,
            "active_catalog_items": active_catalog_items,
            "filters": {
                "q": query,
                "category": category_slug,
                "platform": platform,
                "rank": rank,
                "min_price": min_price,
                "max_price": max_price,
                "game": active_game,
            },
        },
    )


def account_detail(request, slug):
    account = get_object_or_404(GameAccount.objects.select_related("category").prefetch_related("videos"), slug=slug)
    related_accounts = GameAccount.objects.exclude(id=account.id)[:3]
    return render(
        request,
        "market/account_detail.html",
        {
            "account": account,
            "related_accounts": related_accounts,
            "telegram_bot_link": build_telegram_bot_link(account),
            "telegram_contact_link": build_telegram_contact_link(account),
            "telegram_bot_username": settings.TELEGRAM_BOT_USERNAME.strip().lstrip("@"),
            "telegram_contact_username": settings.TELEGRAM_CONTACT_USERNAME.strip().lstrip("@"),
        },
    )


@login_required
def buy_account(request, slug):
    account = get_object_or_404(GameAccount, slug=slug)
    if Purchase.objects.filter(buyer=request.user, account=account).exists():
        messages.info(request, "Siz bu accountni allaqachon sotib olgansiz.")
        return redirect("market:account_detail", slug=slug)

    if request.method == "POST":
        provider = request.POST.get("provider", "")
        if provider not in dict(PaymentTransaction.Provider.choices):
            messages.error(request, "Noto'g'ri payment provider tanlandi.")
            return redirect("market:account_detail", slug=slug)
        if not provider_enabled(provider):
            messages.error(request, f"{provider.title()} merchant parametrlari sozlanmagan.")
            return redirect("market:account_detail", slug=slug)

        transaction = PaymentTransaction.objects.create(
            buyer=request.user,
            account=account,
            provider=provider,
            order_id=secrets.token_hex(12),
            amount=account.price,
        )

        if provider == PaymentTransaction.Provider.STRIPE:
            return redirect(create_stripe_checkout(transaction))
        if provider == PaymentTransaction.Provider.CLICK:
            return redirect(build_click_url(transaction))
        if provider == PaymentTransaction.Provider.PAYME:
            return redirect(build_payme_url(transaction))

    return redirect("market:account_detail", slug=slug)


def signup(request):
    if request.user.is_authenticated:
        return redirect("market:home")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Website account yaratildi. Endi accountlarni sotib olishingiz mumkin.")
        return redirect("market:home")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    purchases = Purchase.objects.select_related("account").filter(buyer=request.user)
    transactions = PaymentTransaction.objects.select_related("account").filter(buyer=request.user)[:20]
    return render(
        request,
        "market/dashboard.html",
        {"purchases": purchases, "transactions": transactions},
    )


def payment_success(request):
    provider = request.GET.get("provider", "")
    session_id = request.GET.get("session_id", "")
    order_id = request.GET.get("order_id", "")
    if provider == PaymentTransaction.Provider.STRIPE and session_id:
        messages.info(request, "Stripe checkout tugadi. Webhook tasdiqlagach access ochiladi.")
    elif order_id:
        messages.info(request, "To'lov yakunlandi. Provider callback tasdiqlagach access ochiladi.")
    return redirect("market:dashboard" if request.user.is_authenticated else "market:home")


def payment_cancel(request):
    order_id = request.GET.get("order_id", "")
    if order_id:
        PaymentTransaction.objects.filter(
            order_id=order_id,
            status=PaymentTransaction.Status.PENDING,
        ).update(status=PaymentTransaction.Status.CANCELLED)
    messages.info(request, "To'lov bekor qilindi.")
    return redirect("market:dashboard" if request.user.is_authenticated else "market:home")


@csrf_exempt
def telegram_webhook(request, token):
    if request.method != "POST":
        return JsonResponse({"detail": "POST only"}, status=405)
    if token != settings.TELEGRAM_BOT_TOKEN.strip():
        return JsonResponse({"detail": "invalid token"}, status=403)
    try:
        payload = json.loads(request.body.decode() or "{}")
        process_update(payload)
    except Exception as exc:
        return JsonResponse({"detail": str(exc)}, status=400)
    return JsonResponse({"ok": True})


@csrf_exempt
def stripe_webhook(request):
    if request.method != "POST":
        return HttpResponse(status=405)
    payload = request.body
    signature = request.headers.get("Stripe-Signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, signature, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        return HttpResponse(status=400)

    if event.get("type") == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session.get("client_reference_id") or session.get("metadata", {}).get("order_id")
        transaction = PaymentTransaction.objects.filter(order_id=order_id).first()
        if transaction:
            mark_transaction_paid(
                transaction,
                external_id=session.get("payment_intent", "") or session.get("id", ""),
                payload={"stripe": session},
            )
    return HttpResponse(status=200)


@csrf_exempt
def click_prepare(request):
    data = request.POST.dict()
    if request.method != "POST" or not verify_click_prepare_signature(data):
        return JsonResponse({"error": -1, "error_note": "signature error"})

    transaction = PaymentTransaction.objects.filter(order_id=data.get("merchant_trans_id", "")).first()
    if not transaction:
        return JsonResponse({"error": -5, "error_note": "transaction not found"})

    transaction.provider_reference = data.get("click_trans_id", "")
    transaction.payload = {**transaction.payload, "click_prepare": data}
    transaction.save(update_fields=["provider_reference", "payload", "updated_at"])

    return JsonResponse(
        {
            "click_trans_id": data.get("click_trans_id"),
            "merchant_trans_id": transaction.order_id,
            "merchant_prepare_id": transaction.id,
            "error": 0,
            "error_note": "Success",
        }
    )


@csrf_exempt
def click_complete(request):
    data = request.POST.dict()
    if request.method != "POST" or not verify_click_complete_signature(data):
        return JsonResponse({"error": -1, "error_note": "signature error"})

    transaction = PaymentTransaction.objects.filter(
        order_id=data.get("merchant_trans_id", ""),
        id=data.get("merchant_prepare_id", "0"),
    ).first()
    if not transaction:
        return JsonResponse({"error": -5, "error_note": "transaction not found"})

    if data.get("error") == "0":
        mark_transaction_paid(transaction, external_id=data.get("click_trans_id", ""), payload={"click_complete": data})
        error_code = 0
        note = "Success"
    else:
        transaction.mark_cancelled(payload={"click_complete": data})
        error_code = -9
        note = "Cancelled"

    return JsonResponse(
        {
            "click_trans_id": data.get("click_trans_id"),
            "merchant_trans_id": transaction.order_id,
            "merchant_confirm_id": transaction.id,
            "error": error_code,
            "error_note": note,
        }
    )


def _payme_error(request_id, code, message, data=None):
    return JsonResponse(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message, "data": data},
        }
    )


@csrf_exempt
def payme_merchant_api(request):
    if request.method != "POST":
        return JsonResponse({"detail": "POST only"}, status=405)

    if settings.PAYME_SECRET_KEY:
        expected = base64.b64encode(f"Paycom:{settings.PAYME_SECRET_KEY}".encode()).decode()
        if request.headers.get("Authorization", "") != f"Basic {expected}":
            return _payme_error(None, -32504, "Insufficient privileges")

    body = json.loads(request.body.decode() or "{}")
    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")

    if method == "CheckPerformTransaction":
        order_id = str(params.get("account", {}).get("order_id", ""))
        amount = Decimal(params.get("amount", 0)) / Decimal("100")
        transaction = PaymentTransaction.objects.filter(
            order_id=order_id,
            provider=PaymentTransaction.Provider.PAYME,
        ).first()
        if not transaction or transaction.amount != amount:
            return _payme_error(request_id, -31050, "Order not found or amount mismatch", "order_id")
        return JsonResponse({"jsonrpc": "2.0", "id": request_id, "result": {"allow": True}})

    if method == "CreateTransaction":
        order_id = str(params.get("account", {}).get("order_id", ""))
        transaction = PaymentTransaction.objects.filter(
            order_id=order_id,
            provider=PaymentTransaction.Provider.PAYME,
        ).first()
        if not transaction:
            return _payme_error(request_id, -31050, "Order not found", "order_id")
        transaction.external_id = params.get("id", "")
        transaction.payload = {**transaction.payload, "payme_create": params}
        transaction.save(update_fields=["external_id", "payload", "updated_at"])
        return JsonResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "create_time": int(transaction.created_at.timestamp() * 1000),
                    "transaction": transaction.order_id,
                    "state": 1,
                },
            }
        )

    if method == "PerformTransaction":
        transaction = PaymentTransaction.objects.filter(external_id=params.get("id", "")).first()
        if not transaction:
            return _payme_error(request_id, -31003, "Transaction not found")
        mark_transaction_paid(transaction, external_id=params.get("id", ""), payload={"payme_perform": params})
        return JsonResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "transaction": transaction.order_id,
                    "perform_time": int(transaction.paid_at.timestamp() * 1000),
                    "state": 2,
                },
            }
        )

    if method == "CancelTransaction":
        transaction = PaymentTransaction.objects.filter(external_id=params.get("id", "")).first()
        if not transaction:
            return _payme_error(request_id, -31003, "Transaction not found")
        transaction.mark_cancelled(payload={"payme_cancel": params})
        return JsonResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "transaction": transaction.order_id,
                    "cancel_time": int(transaction.cancelled_at.timestamp() * 1000),
                    "state": -1,
                },
            }
        )

    if method == "CheckTransaction":
        transaction = PaymentTransaction.objects.filter(external_id=params.get("id", "")).first()
        if not transaction:
            return _payme_error(request_id, -31003, "Transaction not found")
        state = 1
        if transaction.status == PaymentTransaction.Status.PAID:
            state = 2
        elif transaction.status == PaymentTransaction.Status.CANCELLED:
            state = -1
        return JsonResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "create_time": int(transaction.created_at.timestamp() * 1000),
                    "perform_time": int(transaction.paid_at.timestamp() * 1000) if transaction.paid_at else 0,
                    "cancel_time": int(transaction.cancelled_at.timestamp() * 1000) if transaction.cancelled_at else 0,
                    "transaction": transaction.order_id,
                    "state": state,
                    "reason": transaction.payload.get("payme_cancel", {}).get("reason"),
                },
            }
        )

    if method == "GetStatement":
        from_ts = timezone.make_aware(datetime.fromtimestamp(int(params.get("from", 0)) / 1000))
        to_ts = timezone.make_aware(datetime.fromtimestamp(int(params.get("to", 0)) / 1000))
        transactions = PaymentTransaction.objects.filter(
            provider=PaymentTransaction.Provider.PAYME,
            created_at__gte=from_ts,
            created_at__lte=to_ts,
        )
        return JsonResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "transactions": [
                        {
                            "id": item.external_id,
                            "time": int(item.created_at.timestamp() * 1000),
                            "amount": int(item.amount * 100),
                            "account": {"order_id": item.order_id},
                            "create_time": int(item.created_at.timestamp() * 1000),
                            "perform_time": int(item.paid_at.timestamp() * 1000) if item.paid_at else 0,
                            "cancel_time": int(item.cancelled_at.timestamp() * 1000) if item.cancelled_at else 0,
                            "transaction": item.order_id,
                            "state": 2 if item.status == PaymentTransaction.Status.PAID else 1,
                        }
                        for item in transactions
                    ]
                },
            }
        )

    return _payme_error(request_id, -32601, "Method not found")
