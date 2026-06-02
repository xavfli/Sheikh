from django.conf import settings
from django.core.management.base import BaseCommand

from market.telegram_bot import get_bot_config, get_webhook_info, set_webhook, validate_bot_token


class Command(BaseCommand):
    help = "Deploy qilingan website uchun Telegram webhook sozlaydi."

    def handle(self, *args, **options):
        config = get_bot_config()
        try:
            validate_bot_token(config.token)
        except RuntimeError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
            return

        site_url = settings.SITE_URL.rstrip("/")
        webhook_url = f"{site_url}/telegram/webhook/{config.token}/"
        response = set_webhook(webhook_url)
        if not response.get("ok"):
            self.stderr.write(self.style.ERROR(f"Webhook sozlanmadi: {response}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Webhook sozlandi: {webhook_url}"))
        info = get_webhook_info()
        self.stdout.write(str(info))
