from django.urls import path

from .views import (
    MarketLoginView,
    MarketLogoutView,
    account_detail,
    buy_account,
    click_complete,
    click_prepare,
    dashboard,
    home,
    payment_cancel,
    payment_success,
    payme_merchant_api,
    signup,
    stripe_webhook,
    telegram_webhook,
)


app_name = "market"

urlpatterns = [
    path("", home, name="home"),
    path("account/<slug:slug>/", account_detail, name="account_detail"),
    path("account/<slug:slug>/buy/", buy_account, name="buy_account"),
    path("dashboard/", dashboard, name="dashboard"),
    path("payments/success/", payment_success, name="payment_success"),
    path("payments/cancel/", payment_cancel, name="payment_cancel"),
    path("payments/stripe/webhook/", stripe_webhook, name="stripe_webhook"),
    path("payments/click/prepare/", click_prepare, name="click_prepare"),
    path("payments/click/complete/", click_complete, name="click_complete"),
    path("payments/payme/merchant-api/", payme_merchant_api, name="payme_merchant_api"),
    path("telegram/webhook/<str:token>/", telegram_webhook, name="telegram_webhook"),
    path("login/", MarketLoginView.as_view(), name="login"),
    path("logout/", MarketLogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
]
