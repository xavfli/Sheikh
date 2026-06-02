from django.core.management.base import BaseCommand

from market.telegram_bot import get_bot_config, run_polling, validate_bot_token


class Command(BaseCommand):
    help = "Telegram botni long polling orqali ishga tushiradi."

    def handle(self, *args, **options):
        config = get_bot_config()
        try:
            validate_bot_token(config.token)
        except RuntimeError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
            return

        self.stdout.write(self.style.SUCCESS(f"Telegram bot ishga tushdi: @{config.username or 'unknown_bot'}"))
        if config.contact_username:
            self.stdout.write(f"Aloqa username: @{config.contact_username}")
        try:
            run_polling()
        except RuntimeError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
