from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GameAccount(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accounts",
    )
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    region = models.CharField(max_length=50)
    platform = models.CharField(max_length=40)
    rank_tier = models.CharField(max_length=80)
    kd_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    matches_played = models.PositiveIntegerField()
    skins_count = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    short_description = models.CharField(max_length=220)
    description = models.TextField()
    hero_image = models.URLField(blank=True)
    hero_upload = models.ImageField(upload_to="accounts/heroes/", blank=True)
    video_url = models.URLField(blank=True)
    pubg_login = models.CharField(max_length=120)
    pubg_password = models.CharField(max_length=120)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def display_image(self) -> str:
        if self.hero_upload:
            return self.hero_upload.url
        return self.hero_image


class AccountVideo(models.Model):
    account = models.ForeignKey(GameAccount, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=120)
    embed_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to="accounts/videos/", blank=True)
    thumbnail = models.ImageField(upload_to="accounts/video-thumbs/", blank=True)
    duration = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.account.title} - {self.title}"

    @property
    def preview_url(self) -> str:
        if self.video_file:
            return self.video_file.url
        return self.embed_url


class Purchase(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    account = models.ForeignKey(GameAccount, on_delete=models.CASCADE, related_name="purchases")
    price_paid = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("buyer", "account")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.buyer.username} -> {self.account.title}"


class PaymentTransaction(models.Model):
    class Provider(models.TextChoices):
        STRIPE = "stripe", "Stripe"
        CLICK = "click", "Click"
        PAYME = "payme", "Payme"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
        FAILED = "failed", "Failed"

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_transactions")
    account = models.ForeignKey(GameAccount, on_delete=models.CASCADE, related_name="payment_transactions")
    provider = models.CharField(max_length=20, choices=Provider.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    order_id = models.CharField(max_length=64, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    external_id = models.CharField(max_length=140, blank=True)
    provider_reference = models.CharField(max_length=140, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.order_id} - {self.provider}"

    def mark_paid(self, external_id: str = "", payload: dict | None = None):
        if self.status != self.Status.PAID:
            self.status = self.Status.PAID
            self.external_id = external_id or self.external_id
            if payload:
                self.payload = {**self.payload, **payload}
            self.paid_at = timezone.now()
            self.save(update_fields=["status", "external_id", "payload", "paid_at", "updated_at"])
        purchase, _ = Purchase.objects.get_or_create(
            buyer=self.buyer,
            account=self.account,
            defaults={"price_paid": self.amount},
        )
        return purchase

    def mark_cancelled(self, payload: dict | None = None):
        self.status = self.Status.CANCELLED
        if payload:
            self.payload = {**self.payload, **payload}
        self.cancelled_at = timezone.now()
        self.save(update_fields=["status", "payload", "cancelled_at", "updated_at"])


class TelegramProfile(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    telegram_username = models.CharField(max_length=120, blank=True)
    first_name = models.CharField(max_length=120, blank=True)
    language = models.CharField(max_length=5, default="uz")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="telegram_profiles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.chat_id} - {self.telegram_username or self.buyer.username}"
