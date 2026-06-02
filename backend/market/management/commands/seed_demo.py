from django.core.management.base import BaseCommand

from market.models import AccountVideo, Category, GameAccount


ACCOUNTS = [
    {
        "category": "Conqueror",
        "title": "Conqueror Rush Account",
        "region": "Europe",
        "platform": "Steam",
        "rank_tier": "Conqueror",
        "kd_ratio": "5.41",
        "matches_played": 1890,
        "skins_count": 126,
        "level": 84,
        "price": "249.00",
        "short_description": "Conqueror rank, premium skins, elite stats va tayyor gameplay archive bilan.",
        "description": (
            "Yuqori darajadagi PUBG account. Rare skinlar, yaxshi K/D, squad va solo uchun tayyor setup. "
            "Sotib olinmaguncha faqat umumiy ma'lumot ko'rinadi, purchase qilingandan keyin login va parol ochiladi."
        ),
        "hero_image": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1400&q=80",
        "video_url": "https://www.youtube.com/embed/1v2bE0zS8lY",
        "pubg_login": "conqueror_hunter@demo.pubg",
        "pubg_password": "PUBG-Conq-991",
        "is_featured": True,
        "videos": [
            {"title": "Kill Montage", "embed_url": "https://www.youtube.com/embed/1v2bE0zS8lY", "duration": "02:10"},
            {"title": "Inventory Showcase", "embed_url": "https://www.youtube.com/embed/aqz-KE-bpKQ", "duration": "01:22"},
        ],
    },
    {
        "category": "Rank Push",
        "title": "Ace Master Tactical ID",
        "region": "Middle East",
        "platform": "Mobile",
        "rank_tier": "Ace Master",
        "kd_ratio": "4.76",
        "matches_played": 1430,
        "skins_count": 93,
        "level": 77,
        "price": "179.00",
        "short_description": "Ace Master rank, gun skin set, stable stat va gameplay preview videolari bilan.",
        "description": (
            "Mid-high tier account bo'lib, competitive o'yin uchun qulay. Vehicle skinlar, outfitlar va tez progress mavjud. "
            "User site accountga kirib real payment tugagach credential ko'radi."
        ),
        "hero_image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1400&q=80",
        "video_url": "https://www.youtube.com/embed/aqz-KE-bpKQ",
        "pubg_login": "ace.master.demo@pubgmail.com",
        "pubg_password": "AceMaster-447",
        "is_featured": True,
        "videos": [
            {"title": "Rank Push Session", "embed_url": "https://www.youtube.com/embed/aqz-KE-bpKQ", "duration": "03:05"},
        ],
    },
    {
        "category": "Collector",
        "title": "Collector Royale Pack",
        "region": "Asia",
        "platform": "Steam",
        "rank_tier": "Diamond Elite",
        "kd_ratio": "3.98",
        "matches_played": 980,
        "skins_count": 148,
        "level": 69,
        "price": "329.00",
        "short_description": "Rare cosmeticlarga boy collector account, showcase video va batafsil loadout bilan.",
        "description": (
            "Skin sevuvchilar uchun collector ID. Rare crate itemlar, yaxshi progression va tayyor outfit setlar bor. "
            "Purchase qilgandan keyin credential va video archive ochiladi."
        ),
        "hero_image": "https://images.unsplash.com/photo-1486572788966-cfd3df1f5b42?auto=format&fit=crop&w=1400&q=80",
        "video_url": "https://www.youtube.com/embed/ysz5S6PUM-U",
        "pubg_login": "collector.pack@demo.net",
        "pubg_password": "Collector-882",
        "is_featured": True,
        "videos": [
            {"title": "Skin Preview", "embed_url": "https://www.youtube.com/embed/ysz5S6PUM-U", "duration": "04:18"},
        ],
    },
]


class Command(BaseCommand):
    help = "PUBG website uchun demo accountlarni yaratadi."

    def handle(self, *args, **options):
        for item in ACCOUNTS:
            account_data = item.copy()
            category_name = account_data.pop("category")
            videos = account_data.pop("videos")
            category, _ = Category.objects.get_or_create(name=category_name)
            account, _ = GameAccount.objects.update_or_create(
                title=account_data["title"],
                defaults={**account_data, "category": category},
            )
            account.videos.all().delete()
            for video in videos:
                AccountVideo.objects.create(account=account, **video)
        self.stdout.write(self.style.SUCCESS("Demo accountlar yaratildi."))
