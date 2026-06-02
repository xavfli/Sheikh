from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Migrate qiladi va demo PUBG accountlarni yuklaydi."

    def handle(self, *args, **options):
        self.stdout.write("Migratsiyalar ishga tushirildi...")
        call_command("migrate")
        self.stdout.write("Demo accountlar yuklanmoqda...")
        call_command("seed_demo")
        self.stdout.write(self.style.SUCCESS("Loyiha tayyor. Endi python manage.py runserver ishlating."))
