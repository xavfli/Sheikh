import html
import json
import time
from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.urls import reverse

from .models import Category, GameAccount, Purchase, TelegramProfile


BOT_API_BASE = "https://api.telegram.org"

LANGUAGES = ("uz", "ru", "en")

BOT_TEXT = {
    "uz": {
        "choose_language": "Tilni tanlang:",
        "welcome": "Sheikh botiga xush kelibsiz. Quyidan kerakli bo'limni tanlang.",
        "menu_catalog": "Katalog",
        "menu_featured": "Mashhur accountlar",
        "menu_purchases": "Mening accountlarim",
        "menu_contact": "Bog'lanish",
        "menu_back": "Ortga",
        "menu_buy": "Sotib olish",
        "menu_pay_uz": "O'zbekiston uchun to'lov",
        "menu_pay_global": "Boshqa davlatlar uchun to'lov",
        "menu_video": "Video preview",
        "menu_contact_manager": "Lichkaga yozish",
        "menu_change_lang": "Tilni almashtirish",
        "catalog_title": "Kategoriya tanlang:",
        "featured_title": "Mashhur accountlar:",
        "accounts_empty": "Hozircha account topilmadi.",
        "category_accounts": "{category} bo'limidagi accountlar:",
        "account_not_found": "Account topilmadi.",
        "bought_success": "Sotib olindi. Login va parol pastda ochildi.",
        "already_bought": "Bu account sizda allaqachon mavjud.",
        "my_purchases_empty": "Siz hali account sotib olmagansiz.",
        "my_purchases_title": "Sotib olingan accountlar:",
        "contact_text": "Menejer bilan bog'lanish uchun tugmani bosing: @{username}",
        "help_text": "Buyruqlar:\n/start\n/catalog\n/featured\n/purchases\n/language",
        "credentials": "Login: <code>{login}</code>\nParol: <code>{password}</code>",
        "account_header": "<b>{title}</b>\nNarxi: <b>${price}</b>\nCategory: {category}\nPlatforma: {platform}\nRegion: {region}\nRank: {rank}\nK/D: {kd}\nLevel: {level}\nSkinlar: {skins}\n\n{description}",
        "buy_notice": "Sotib olgandan keyin login va parol bot ichida ko'rsatiladi.",
        "payment_title": "<b>{title}</b>\n\nTo'lov turini tanlang. Menejer buyurtmani tasdiqlagandan keyin login va parol botda ochiladi.",
        "payment_uz": "O'zbekiston uchun tavsiya: Payme yoki Click. Tugmani bosing va menejerga tayyor buyurtma bilan yozing.",
        "payment_global": "Boshqa davlatlar uchun tavsiya: Stripe yoki xalqaro transfer. Tugmani bosing va menejerga tayyor buyurtma bilan yozing.",
        "manager_order": "Menejerga buyurtma yuborish",
    },
    "ru": {
        "choose_language": "Выберите язык:",
        "welcome": "Добро пожаловать в Sheikh. Выберите нужный раздел ниже.",
        "menu_catalog": "Каталог",
        "menu_featured": "Популярные аккаунты",
        "menu_purchases": "Мои аккаунты",
        "menu_contact": "Связь",
        "menu_back": "Назад",
        "menu_buy": "Купить",
        "menu_pay_uz": "Оплата для Узбекистана",
        "menu_pay_global": "Оплата для других стран",
        "menu_video": "Видео preview",
        "menu_contact_manager": "Написать менеджеру",
        "menu_change_lang": "Сменить язык",
        "catalog_title": "Выберите категорию:",
        "featured_title": "Популярные аккаунты:",
        "accounts_empty": "Аккаунты пока не найдены.",
        "category_accounts": "Аккаунты в разделе {category}:",
        "account_not_found": "Аккаунт не найден.",
        "bought_success": "Покупка выполнена. Логин и пароль открыты ниже.",
        "already_bought": "Этот аккаунт уже есть у вас.",
        "my_purchases_empty": "Вы пока не купили ни одного аккаунта.",
        "my_purchases_title": "Купленные аккаунты:",
        "contact_text": "Для связи с менеджером нажмите кнопку: @{username}",
        "help_text": "Команды:\n/start\n/catalog\n/featured\n/purchases\n/language",
        "credentials": "Логин: <code>{login}</code>\nПароль: <code>{password}</code>",
        "account_header": "<b>{title}</b>\nЦена: <b>${price}</b>\nКатегория: {category}\nПлатформа: {platform}\nРегион: {region}\nРанг: {rank}\nK/D: {kd}\nУровень: {level}\nСкины: {skins}\n\n{description}",
        "buy_notice": "После покупки логин и пароль будут показаны прямо в боте.",
        "payment_title": "<b>{title}</b>\n\nВыберите тип оплаты. После подтверждения менеджером логин и пароль откроются в боте.",
        "payment_uz": "Для Узбекистана рекомендуются Payme или Click. Нажмите кнопку и отправьте менеджеру готовый заказ.",
        "payment_global": "Для других стран рекомендуются Stripe или международный перевод. Нажмите кнопку и отправьте менеджеру готовый заказ.",
        "manager_order": "Отправить заказ менеджеру",
    },
    "en": {
        "choose_language": "Choose a language:",
        "welcome": "Welcome to Sheikh. Choose a section below.",
        "menu_catalog": "Catalog",
        "menu_featured": "Featured accounts",
        "menu_purchases": "My accounts",
        "menu_contact": "Contact",
        "menu_back": "Back",
        "menu_buy": "Buy now",
        "menu_pay_uz": "Uzbekistan payment",
        "menu_pay_global": "International payment",
        "menu_video": "Video preview",
        "menu_contact_manager": "Message manager",
        "menu_change_lang": "Change language",
        "catalog_title": "Choose a category:",
        "featured_title": "Featured accounts:",
        "accounts_empty": "No accounts found yet.",
        "category_accounts": "Accounts in {category}:",
        "account_not_found": "Account not found.",
        "bought_success": "Purchase completed. Login and password are shown below.",
        "already_bought": "You already own this account.",
        "my_purchases_empty": "You have not bought any accounts yet.",
        "my_purchases_title": "Purchased accounts:",
        "contact_text": "Tap the button to contact the manager: @{username}",
        "help_text": "Commands:\n/start\n/catalog\n/featured\n/purchases\n/language",
        "credentials": "Login: <code>{login}</code>\nPassword: <code>{password}</code>",
        "account_header": "<b>{title}</b>\nPrice: <b>${price}</b>\nCategory: {category}\nPlatform: {platform}\nRegion: {region}\nRank: {rank}\nK/D: {kd}\nLevel: {level}\nSkins: {skins}\n\n{description}",
        "buy_notice": "After purchase, the login and password will be revealed in the bot.",
        "payment_title": "<b>{title}</b>\n\nChoose a payment route. Login and password will be revealed in the bot after manager confirmation.",
        "payment_uz": "Recommended for Uzbekistan: Payme or Click. Tap the button and send the prepared order to the manager.",
        "payment_global": "Recommended for other countries: Stripe or international transfer. Tap the button and send the prepared order to the manager.",
        "manager_order": "Send order to manager",
    },
}


@dataclass
class TelegramBotConfig:
    token: str
    username: str
    contact_username: str
    site_url: str


def text_for(language: str, key: str, **kwargs) -> str:
    language = language if language in BOT_TEXT else "uz"
    return BOT_TEXT[language][key].format(**kwargs)


def get_bot_config() -> TelegramBotConfig:
    return TelegramBotConfig(
        token=settings.TELEGRAM_BOT_TOKEN.strip(),
        username=settings.TELEGRAM_BOT_USERNAME.strip().lstrip("@"),
        contact_username=settings.TELEGRAM_CONTACT_USERNAME.strip().lstrip("@"),
        site_url=settings.SITE_URL.rstrip("/"),
    )


def validate_bot_token(token: str):
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN topilmadi. BotFather tokenini env ga qo'ying.")
    if " " in token or "\n" in token or "\r" in token or ":" not in token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN noto'g'ri ko'rinadi. "
            "BotFather bergan haqiqiy token formatini kiriting, masalan: 123456:ABCdef..."
        )


def api_request(method: str, payload: dict):
    config = get_bot_config()
    validate_bot_token(config.token)
    data = urlencode(payload).encode()
    try:
        with urlopen(f"{BOT_API_BASE}/bot{config.token}/{method}", data=data, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as exc:
        body = exc.read().decode(errors="ignore")
        if exc.code == 400:
            raise RuntimeError(f"Telegram 400 Bad Request: {body}") from exc
        raise


def send_message(chat_id: int | str, text: str, reply_markup: dict | None = None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
    return api_request("sendMessage", payload)


def edit_message(chat_id: int | str, message_id: int, text: str, reply_markup: dict | None = None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
    return api_request("editMessageText", payload)


def answer_callback(callback_query_id: str):
    return api_request("answerCallbackQuery", {"callback_query_id": callback_query_id})


def set_webhook(webhook_url: str):
    return api_request("setWebhook", {"url": webhook_url})


def delete_webhook():
    return api_request("deleteWebhook", {"drop_pending_updates": "false"})


def get_webhook_info():
    config = get_bot_config()
    validate_bot_token(config.token)
    with urlopen(f"{BOT_API_BASE}/bot{config.token}/getWebhookInfo", timeout=30) as response:
        return json.loads(response.read().decode())


def get_or_create_profile(chat: dict, from_user: dict | None = None) -> TelegramProfile:
    chat_id = chat["id"]
    from_user = from_user or {}
    username = from_user.get("username", "")
    first_name = from_user.get("first_name", "")
    buyer_username = f"tg_{chat_id}"
    buyer, _ = User.objects.get_or_create(
        username=buyer_username,
        defaults={"first_name": first_name[:150]},
    )
    buyer.set_unusable_password()
    buyer.save(update_fields=["password"])
    profile, _ = TelegramProfile.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            "telegram_username": username,
            "first_name": first_name,
            "buyer": buyer,
        },
    )
    updated = False
    if profile.telegram_username != username:
        profile.telegram_username = username
        updated = True
    if profile.first_name != first_name:
        profile.first_name = first_name
        updated = True
    if profile.buyer_id != buyer.id:
        profile.buyer = buyer
        updated = True
    if updated:
        profile.save()
    return profile


def set_profile_language(profile: TelegramProfile, language: str):
    if language in LANGUAGES and profile.language != language:
        profile.language = language
        profile.save(update_fields=["language", "updated_at"])


def language_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "O'zbekcha", "callback_data": "lang:uz"},
                {"text": "Русский", "callback_data": "lang:ru"},
                {"text": "English", "callback_data": "lang:en"},
            ]
        ]
    }


def main_menu_keyboard(language: str) -> dict:
    return {
        "inline_keyboard": [
            [{"text": text_for(language, "menu_catalog"), "callback_data": "menu:catalog"}],
            [{"text": text_for(language, "menu_featured"), "callback_data": "menu:featured"}],
            [{"text": text_for(language, "menu_purchases"), "callback_data": "menu:purchases"}],
            [{"text": text_for(language, "menu_contact"), "callback_data": "menu:contact"}],
            [{"text": text_for(language, "menu_change_lang"), "callback_data": "menu:language"}],
        ]
    }


def back_menu_row(language: str) -> list[dict]:
    return [{"text": text_for(language, "menu_back"), "callback_data": "menu:home"}]


def categories_keyboard(language: str) -> dict:
    rows = []
    for category in Category.objects.all():
        rows.append([{"text": category.name, "callback_data": f"category:{category.slug}"}])
    rows.append(back_menu_row(language))
    return {"inline_keyboard": rows}


def accounts_keyboard(accounts: QuerySet[GameAccount], language: str, back_target: str) -> dict:
    rows = [[{"text": account.title[:40], "callback_data": f"account:{account.slug}"}] for account in accounts]
    rows.append([{"text": text_for(language, "menu_back"), "callback_data": back_target}])
    return {"inline_keyboard": rows}


def build_account_text(account: GameAccount, language: str, include_credentials: bool = False) -> str:
    category = html.escape(account.category.name) if account.category else "General"
    text = text_for(
        language,
        "account_header",
        title=html.escape(account.title),
        price=account.price,
        category=category,
        platform=html.escape(account.platform),
        region=html.escape(account.region),
        rank=html.escape(account.rank_tier),
        kd=account.kd_ratio,
        level=account.level,
        skins=account.skins_count,
        description=html.escape(account.description),
    )
    if include_credentials:
        text += "\n\n" + text_for(
            language,
            "credentials",
            login=html.escape(account.pubg_login),
            password=html.escape(account.pubg_password),
        )
    else:
        text += "\n\n" + text_for(language, "buy_notice")
    return text


def account_keyboard(account: GameAccount, language: str, purchased: bool = False) -> dict:
    config = get_bot_config()
    rows = []
    if not purchased:
        rows.append([{"text": text_for(language, "menu_buy"), "callback_data": f"pay:{account.slug}"}])
    if account.video_url:
        rows.append([{"text": text_for(language, "menu_video"), "url": account.video_url}])
    elif account.videos.exists():
        video = account.videos.first()
        if video and video.preview_url:
            rows.append([{"text": text_for(language, "menu_video"), "url": video.preview_url}])
    if config.contact_username:
        rows.append(
            [
                {
                    "text": text_for(language, "menu_contact_manager"),
                    "url": f"https://t.me/{config.contact_username}",
                }
            ]
        )
    rows.append(back_menu_row(language))
    return {"inline_keyboard": rows}


def manager_order_url(account: GameAccount, payment_route: str) -> str:
    contact_username = get_bot_config().contact_username
    if not contact_username:
        return ""
    route_label = "O'zbekiston: Payme/Click" if payment_route == "uz" else "International: Stripe/transfer"
    message = (
        f"Sotib olmoqchiman:\n"
        f"Account: {account.title}\n"
        f"Narxi: {account.price}$\n"
        f"To'lov: {route_label}\n"
        f"Platforma: {account.platform}\n"
        f"Region: {account.region}\n"
        f"Rank: {account.rank_tier}"
    )
    return f"https://t.me/{contact_username}?text={urlencode({'': message})[1:]}"


def payment_keyboard(account: GameAccount, language: str, route: str | None = None) -> dict:
    rows = []
    if route:
        manager_url = manager_order_url(account, route)
        if manager_url:
            rows.append([{"text": text_for(language, "manager_order"), "url": manager_url}])
    else:
        rows.append([{"text": text_for(language, "menu_pay_uz"), "callback_data": f"payroute:uz:{account.slug}"}])
        rows.append([{"text": text_for(language, "menu_pay_global"), "callback_data": f"payroute:global:{account.slug}"}])
    rows.append([{"text": text_for(language, "menu_back"), "callback_data": f"account:{account.slug}"}])
    return {"inline_keyboard": rows}


def send_main_menu(chat_id: int | str, language: str):
    return send_message(chat_id, text_for(language, "welcome"), main_menu_keyboard(language))


def edit_main_menu(chat_id: int | str, message_id: int, language: str):
    return edit_message(chat_id, message_id, text_for(language, "welcome"), main_menu_keyboard(language))


def handle_catalog(chat_id: int | str, message_id: int, language: str):
    return edit_message(chat_id, message_id, text_for(language, "catalog_title"), categories_keyboard(language))


def handle_featured(chat_id: int | str, message_id: int, language: str):
    accounts = GameAccount.objects.filter(is_featured=True).select_related("category").prefetch_related("videos")
    if not accounts.exists():
        return edit_message(chat_id, message_id, text_for(language, "accounts_empty"), {"inline_keyboard": [back_menu_row(language)]})
    return edit_message(
        chat_id,
        message_id,
        text_for(language, "featured_title"),
        accounts_keyboard(accounts, language, "menu:home"),
    )


def handle_category(chat_id: int | str, message_id: int, slug: str, language: str):
    category = Category.objects.filter(slug=slug).first()
    if not category:
        return edit_message(chat_id, message_id, text_for(language, "accounts_empty"), {"inline_keyboard": [back_menu_row(language)]})
    accounts = GameAccount.objects.filter(category=category).select_related("category").prefetch_related("videos")
    if not accounts.exists():
        return edit_message(chat_id, message_id, text_for(language, "accounts_empty"), {"inline_keyboard": [back_menu_row(language)]})
    return edit_message(
        chat_id,
        message_id,
        text_for(language, "category_accounts", category=html.escape(category.name)),
        accounts_keyboard(accounts, language, "menu:catalog"),
    )


def handle_account(chat_id: int | str, message_id: int, profile: TelegramProfile, slug: str):
    account = GameAccount.objects.select_related("category").prefetch_related("videos").filter(slug=slug).first()
    if not account:
        return edit_message(chat_id, message_id, text_for(profile.language, "account_not_found"), {"inline_keyboard": [back_menu_row(profile.language)]})
    purchased = Purchase.objects.filter(buyer=profile.buyer, account=account).exists()
    return edit_message(
        chat_id,
        message_id,
        build_account_text(account, profile.language, include_credentials=purchased),
        account_keyboard(account, profile.language, purchased=purchased),
    )


def handle_buy(chat_id: int | str, message_id: int, profile: TelegramProfile, slug: str):
    account = GameAccount.objects.select_related("category").prefetch_related("videos").filter(slug=slug).first()
    if not account:
        return edit_message(chat_id, message_id, text_for(profile.language, "account_not_found"), {"inline_keyboard": [back_menu_row(profile.language)]})
    purchase, created = Purchase.objects.get_or_create(
        buyer=profile.buyer,
        account=account,
        defaults={"price_paid": account.price},
    )
    notice = text_for(profile.language, "bought_success") if created else text_for(profile.language, "already_bought")
    text = build_account_text(account, profile.language, include_credentials=True) + "\n\n" + notice
    return edit_message(chat_id, message_id, text, account_keyboard(account, profile.language, purchased=True))


def handle_payment_choice(chat_id: int | str, message_id: int, profile: TelegramProfile, slug: str, route: str | None = None):
    account = GameAccount.objects.select_related("category").prefetch_related("videos").filter(slug=slug).first()
    if not account:
        return edit_message(chat_id, message_id, text_for(profile.language, "account_not_found"), {"inline_keyboard": [back_menu_row(profile.language)]})
    text = text_for(profile.language, "payment_title", title=html.escape(account.title))
    if route == "uz":
        text += "\n\n" + text_for(profile.language, "payment_uz")
    elif route == "global":
        text += "\n\n" + text_for(profile.language, "payment_global")
    return edit_message(chat_id, message_id, text, payment_keyboard(account, profile.language, route=route))


def find_account_by_start_payload(payload: str) -> GameAccount | None:
    if payload.startswith("buy_"):
        account_id = payload.replace("buy_", "", 1)
        if account_id.isdigit():
            return GameAccount.objects.select_related("category").prefetch_related("videos").filter(id=account_id).first()
    return GameAccount.objects.select_related("category").prefetch_related("videos").filter(slug=payload).first()


def handle_purchases(chat_id: int | str, message_id: int, profile: TelegramProfile):
    purchases = Purchase.objects.filter(buyer=profile.buyer).select_related("account__category")
    if not purchases.exists():
        return edit_message(chat_id, message_id, text_for(profile.language, "my_purchases_empty"), {"inline_keyboard": [back_menu_row(profile.language)]})
    lines = [text_for(profile.language, "my_purchases_title"), ""]
    rows = []
    for purchase in purchases:
        lines.append(f"• {html.escape(purchase.account.title)} — ${purchase.price_paid}")
        rows.append([{"text": purchase.account.title[:40], "callback_data": f"account:{purchase.account.slug}"}])
    rows.append(back_menu_row(profile.language))
    return edit_message(chat_id, message_id, "\n".join(lines), {"inline_keyboard": rows})


def handle_contact(chat_id: int | str, message_id: int, language: str):
    contact_username = get_bot_config().contact_username or "khVO1D"
    return edit_message(
        chat_id,
        message_id,
        text_for(language, "contact_text", username=html.escape(contact_username)),
        {
            "inline_keyboard": [
                [{"text": text_for(language, "menu_contact_manager"), "url": f"https://t.me/{contact_username}"}],
                back_menu_row(language),
            ]
        },
    )


def handle_text_message(message: dict):
    profile = get_or_create_profile(message["chat"], message.get("from"))
    chat_id = message["chat"]["id"]
    normalized = (message.get("text") or "").strip()

    if normalized.startswith("/start"):
        parts = normalized.split(maxsplit=1)
        payload = parts[1].strip() if len(parts) > 1 else ""
        if payload in LANGUAGES:
            set_profile_language(profile, payload)
            return send_main_menu(chat_id, payload)
        if payload:
            account = find_account_by_start_payload(payload)
            if account:
                purchased = Purchase.objects.filter(buyer=profile.buyer, account=account).exists()
                return send_message(chat_id, build_account_text(account, profile.language, include_credentials=purchased), account_keyboard(account, profile.language, purchased=purchased))
        return send_message(chat_id, text_for(profile.language, "choose_language"), language_keyboard())

    if normalized.startswith("/catalog"):
        return send_message(chat_id, text_for(profile.language, "catalog_title"), categories_keyboard(profile.language))
    if normalized.startswith("/featured"):
        accounts = GameAccount.objects.filter(is_featured=True).select_related("category").prefetch_related("videos")
        if not accounts.exists():
            return send_message(chat_id, text_for(profile.language, "accounts_empty"), {"inline_keyboard": [back_menu_row(profile.language)]})
        return send_message(chat_id, text_for(profile.language, "featured_title"), accounts_keyboard(accounts, profile.language, "menu:home"))
    if normalized.startswith("/purchases"):
        purchases = Purchase.objects.filter(buyer=profile.buyer).select_related("account")
        if not purchases.exists():
            return send_message(chat_id, text_for(profile.language, "my_purchases_empty"), {"inline_keyboard": [back_menu_row(profile.language)]})
        lines = [text_for(profile.language, "my_purchases_title"), ""]
        rows = []
        for purchase in purchases:
            lines.append(f"• {html.escape(purchase.account.title)} — ${purchase.price_paid}")
            rows.append([{"text": purchase.account.title[:40], "callback_data": f"account:{purchase.account.slug}"}])
        rows.append(back_menu_row(profile.language))
        return send_message(chat_id, "\n".join(lines), {"inline_keyboard": rows})
    if normalized.startswith("/language"):
        return send_message(chat_id, text_for(profile.language, "choose_language"), language_keyboard())
    if normalized.startswith("/account"):
        slug = normalized.replace("/account", "", 1).strip()
        if not slug:
            return send_message(chat_id, text_for(profile.language, "help_text"))
        account = GameAccount.objects.select_related("category").prefetch_related("videos").filter(slug=slug).first()
        if not account:
            return send_message(chat_id, text_for(profile.language, "account_not_found"))
        purchased = Purchase.objects.filter(buyer=profile.buyer, account=account).exists()
        return send_message(chat_id, build_account_text(account, profile.language, include_credentials=purchased), account_keyboard(account, profile.language, purchased=purchased))
    return send_message(chat_id, text_for(profile.language, "help_text"), main_menu_keyboard(profile.language))


def handle_callback(callback: dict):
    message = callback["message"]
    profile = get_or_create_profile(message["chat"], callback.get("from"))
    data = callback.get("data", "")
    chat_id = message["chat"]["id"]
    message_id = message["message_id"]
    answer_callback(callback["id"])

    if data.startswith("lang:"):
        language = data.split(":", 1)[1]
        set_profile_language(profile, language)
        return edit_main_menu(chat_id, message_id, profile.language)
    if data == "menu:home":
        return edit_main_menu(chat_id, message_id, profile.language)
    if data == "menu:language":
        return edit_message(chat_id, message_id, text_for(profile.language, "choose_language"), language_keyboard())
    if data == "menu:catalog":
        return handle_catalog(chat_id, message_id, profile.language)
    if data == "menu:featured":
        return handle_featured(chat_id, message_id, profile.language)
    if data == "menu:purchases":
        return handle_purchases(chat_id, message_id, profile)
    if data == "menu:contact":
        return handle_contact(chat_id, message_id, profile.language)
    if data.startswith("category:"):
        return handle_category(chat_id, message_id, data.split(":", 1)[1], profile.language)
    if data.startswith("account:"):
        return handle_account(chat_id, message_id, profile, data.split(":", 1)[1])
    if data.startswith("payroute:"):
        _, route, slug = data.split(":", 2)
        return handle_payment_choice(chat_id, message_id, profile, slug, route=route)
    if data.startswith("pay:"):
        return handle_payment_choice(chat_id, message_id, profile, data.split(":", 1)[1])
    if data.startswith("buy:"):
        return handle_buy(chat_id, message_id, profile, data.split(":", 1)[1])


def process_update(update: dict):
    if "message" in update and update["message"].get("text"):
        handle_text_message(update["message"])
    elif "callback_query" in update:
        handle_callback(update["callback_query"])


def run_polling():
    offset = 0
    config = get_bot_config()
    validate_bot_token(config.token)
    while True:
        query = urlencode({"timeout": 25, "offset": offset})
        try:
            with urlopen(f"{BOT_API_BASE}/bot{config.token}/getUpdates?{query}", timeout=35) as response:
                data = json.loads(response.read().decode())
        except HTTPError as exc:
            if exc.code == 401:
                raise RuntimeError(
                    "Telegram 401 Unauthorized: TELEGRAM_BOT_TOKEN haqiqiy emas yoki bekor qilingan. "
                    "BotFather bergan haqiqiy tokenni qo'ying."
                ) from exc
            body = exc.read().decode(errors="ignore")
            raise RuntimeError(f"Telegram HTTP error: {body}") from exc

        for update in data.get("result", []):
            offset = update["update_id"] + 1
            process_update(update)

        time.sleep(1)
