from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GameAccount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=140)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("region", models.CharField(max_length=50)),
                ("platform", models.CharField(max_length=40)),
                ("rank_tier", models.CharField(max_length=80)),
                ("kd_ratio", models.DecimalField(decimal_places=2, max_digits=4)),
                ("matches_played", models.PositiveIntegerField()),
                ("skins_count", models.PositiveIntegerField()),
                ("level", models.PositiveIntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("short_description", models.CharField(max_length=220)),
                ("description", models.TextField()),
                ("hero_image", models.URLField()),
                ("video_url", models.URLField(blank=True)),
                ("pubg_login", models.CharField(max_length=120)),
                ("pubg_password", models.CharField(max_length=120)),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-is_featured", "-created_at"]},
        ),
        migrations.CreateModel(
            name="AccountVideo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("embed_url", models.URLField()),
                ("duration", models.CharField(blank=True, max_length=20)),
                (
                    "account",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="videos", to="market.gameaccount"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Purchase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price_paid", models.DecimalField(decimal_places=2, max_digits=8)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "account",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="purchases", to="market.gameaccount"),
                ),
                (
                    "buyer",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="purchases", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-created_at"], "unique_together": {("buyer", "account")}},
        ),
    ]
