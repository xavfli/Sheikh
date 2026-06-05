import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Environment variablelar orqali production admin foydalanuvchisini yaratadi."

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin").strip()
        email = os.environ.get("ADMIN_EMAIL", "admin@sheikh.uz").strip()
        password = os.environ.get("ADMIN_PASSWORD", "").strip()

        if not password:
            raise CommandError("ADMIN_PASSWORD topilmadi. Render Environment ichiga maxfiy parol kiriting.")

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        status = "yaratildi" if created else "yangilandi"
        self.stdout.write(self.style.SUCCESS(f"Admin '{username}' {status}."))
