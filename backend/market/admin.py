from django.contrib import admin
from django.utils.html import format_html

from .models import AccountVideo, Category, GameAccount, PaymentTransaction, Purchase


class AccountVideoInline(admin.TabularInline):
    model = AccountVideo
    extra = 1


@admin.register(GameAccount)
class GameAccountAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "platform", "region", "rank_tier", "price", "is_featured", "preview")
    list_filter = ("category", "platform", "region", "is_featured")
    search_fields = ("title", "rank_tier", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [AccountVideoInline]

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.hero_upload:
            return format_html('<img src="{}" style="height:48px;border-radius:10px;" />', obj.hero_upload.url)
        if obj.hero_image:
            return format_html('<img src="{}" style="height:48px;border-radius:10px;" />', obj.hero_image)
        return "-"


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("buyer", "account", "price_paid", "created_at")
    search_fields = ("buyer__username", "account__title")


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("order_id", "buyer", "account", "provider", "status", "amount", "created_at")
    list_filter = ("provider", "status")
    search_fields = ("order_id", "buyer__username", "account__title", "external_id")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(AccountVideo)
