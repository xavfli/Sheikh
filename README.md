# Sheikh

`Sheikh` bu `Django` asosida qilingan premium gaming account showcase loyihasi. Endi savdo website login orqali emas, `Telegram bot` va `Telegram lichka` orqali qilinadi.

## Tuzilishi

- `backend/` - Django backend, model, admin, route va management commandlar
- `frontend/` - template, CSS va JavaScript frontend
- `manage.py` - barcha asosiy komandalar uchun root entry point

## Asosiy imkoniyatlar

- PUBG account showcase, qidiruv, filter va premium UI
- admin panelda rasm upload va video boshqarish
- account detail sahifasida video preview va to'liq account ma'lumotlari
- `Telegram bot` orqali account bo'yicha tayyor buyurtma xabari
- `Telegram lichka` orqali to'g'ridan-to'g'ri bog'lanish
- premium animatsiyalar, glow effektlar va responsive layout

## Ishga tushirish

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py setup_demo
python manage.py runserver
```

Brauzerda `http://127.0.0.1:8000` ni oching.

## Admin

```bash
python manage.py createsuperuser
```

So'ng `http://127.0.0.1:8000/admin/` orqali accountlar, rasmlar va videolarni boshqarishingiz mumkin.

## Telegram Bot

Loyiha ichida tayyor Telegram bot komandasi bor:

```bash
python manage.py run_telegram_bot
```

Deploy qilingan website uchun eng yaxshi variant webhook:

```bash
python manage.py set_telegram_webhook
```

Bot quyidagilarni qiladi:

- `/start` - welcome va accountlar ro'yxati
- `/accounts` - accountlar ro'yxati
- `/account <slug>` - bitta account bo'yicha narx, rank, video link va bog'lanish tugmalari
- inline tugmalar orqali account detail ko'rsatadi

## Bot yaratish

Telegram botni men to'g'ridan-to'g'ri yaratib bera olmayman, chunki bu `BotFather` ichida sizning Telegram accountingiz orqali qilinadi. Lekin quyidagi qadam bilan 2 daqiqada tayyor bo'ladi:

1. Telegram ichida `@BotFather` ga kiring
2. `/newbot` yuboring
3. Bot nomi va username bering
4. Berilgan tokenni nusxalang

Keyin env qiymatlarini qo'ying:

```powershell
copy .env.example .env
```

Eslatma:

- `TELEGRAM_BOT_TOKEN` ichida bo'sh joy bo'lmasligi kerak
- token odatda `123456789:ABC...` ko'rinishida bo'ladi
- `BotFather token` degan matnni aynan o'zini yozmang, uning o'rniga BotFather bergan haqiqiy tokenni qo'ying

So'ng `.env` ichini to'ldiring:

```env
SITE_URL=http://127.0.0.1:8000
TELEGRAM_BOT_TOKEN=123456789:AAExampleRealBotFatherToken
TELEGRAM_BOT_USERNAME=sizning_bot_username
TELEGRAM_CONTACT_USERNAME=sizning_username
```

Keyin botni ishga tushiring:

```bash
python manage.py run_telegram_bot
```

Yoki Windows uchun tayyor fayl:

```bash
.\start_bot.bat
```

Website va botni birga ishga tushirish uchun:

```bash
.\start_all.bat
```

Production tavsiya:

- lokalda `run_telegram_bot` ishlating
- hostingga chiqganda `set_telegram_webhook` ishlating
- shunda website deploy bo'lsa bot ham shu saytdan avtomatik ishlaydi

## Production `.env`

Hostingga joylaganda `.env` taxminan shunday bo'ladi:

```env
SITE_URL=https://your-domain.com
SECRET_KEY=very-long-random-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com

TELEGRAM_BOT_TOKEN=123456789:REAL_BOTFATHER_TOKEN
TELEGRAM_BOT_USERNAME=sheikh_pbot
TELEGRAM_CONTACT_USERNAME=khVO1D
```

Eslatma:

- `SITE_URL` albatta `https://` bilan boshlansin
- `ALLOWED_HOSTS` ichiga domainingizni yozing
- `CSRF_TRUSTED_ORIGINS` ham `https://domain.com` formatida bo'lsin
- `DEBUG=False` production uchun kerak
- haqiqiy tokenni chatga yoki public joyga chiqarmang

## Webhook Ulash

Webhook productionda botni avtomatik ishlatadi. Bunda alohida `run_telegram_bot` oynasi ochiq turishi shart emas, Telegram update'lar to'g'ridan-to'g'ri websayt endpointiga keladi.

Deploydan keyin serverda shu komandani ishlating:

```bash
python manage.py set_telegram_webhook
```

U quyidagi ko'rinishdagi webhook URL'ni Telegramga ulaydi:

```text
https://your-domain.com/telegram/webhook/<TELEGRAM_BOT_TOKEN>/
```

Webhook ishlashi uchun:

- domain public internetda ochiq bo'lishi kerak
- HTTPS bo'lishi kerak
- `SITE_URL=https://your-domain.com` to'g'ri yozilgan bo'lishi kerak
- `TELEGRAM_BOT_TOKEN` haqiqiy BotFather token bo'lishi kerak

## Domain Bilan Deploy Ketma-ketligi

1. Hosting serverga loyiha fayllarini joylang
2. Python virtual environment yarating
3. Dependency'larni o'rnating

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux hostingda activate odatda shunday bo'ladi:

```bash
source .venv/bin/activate
```

4. Production `.env` ni to'ldiring

```env
SITE_URL=https://your-domain.com
SECRET_KEY=very-long-random-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
TELEGRAM_BOT_TOKEN=123456789:REAL_BOTFATHER_TOKEN
TELEGRAM_BOT_USERNAME=sheikh_pbot
TELEGRAM_CONTACT_USERNAME=khVO1D
```

5. Database migrationlarni bajaring

```bash
python manage.py migrate
```

6. Static fayllarni yig'ing

```bash
python manage.py collectstatic
```

7. Admin user yarating

```bash
python manage.py createsuperuser
```

8. Web serverni Django appga ulang

Gunicorn/Uvicorn, Nginx yoki hosting paneldagi Python app sozlamasidan foydalaning. Entry point:

```text
backend/config/wsgi.py
```

9. Domain va HTTPS ishlayotganini tekshiring

```text
https://your-domain.com
```

10. Telegram webhookni ulang

```bash
python manage.py set_telegram_webhook
```

11. Botni Telegramda tekshiring

```text
/start
```

Shundan keyin admin panelda account qo'shsangiz yoki o'zgartirsangiz, bot ham shu bazadan avtomatik yangi ma'lumotni ko'radi.

## Render Free Deploy

Render uchun loyiha ichida tayyor fayllar bor:

- `render.yaml` - Render blueprint sozlamasi
- `build.sh` - dependency, static va migration build komandasi
- `requirements.txt` - `gunicorn`, `whitenoise`, `dj-database-url` va Postgres driver bilan

Render panelda eng oson yo'l:

1. GitHub repo `https://github.com/xavfli/Sheikh.git` ni Renderga ulang
2. `New +` -> `Blueprint` yoki `Web Service` tanlang
3. Agar `Blueprint` tanlasangiz, Render `render.yaml` ni o'zi o'qiydi
4. Agar `Web Service` tanlasangiz, quyidagilarni qo'lda kiriting

```bash
Build Command:
bash build.sh

Start Command:
gunicorn --pythonpath backend config.wsgi:application
```

Render environment variables:

```env
DEBUG=False
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
TELEGRAM_BOT_TOKEN=BotFather_bergan_haqiqiy_token
TELEGRAM_BOT_USERNAME=sheikh_pbot
TELEGRAM_CONTACT_USERNAME=khVO1D
```

`SITE_URL` ni Render URL chiqqandan keyin qo'ying:

```env
SITE_URL=https://your-render-service.onrender.com
```

`SECRET_KEY` ni Render blueprint avtomatik generate qiladi. Agar qo'lda deploy qilsangiz, Render env ichida kuchli random qiymat bering.

Deploydan keyin:

```bash
python manage.py createsuperuser
python manage.py set_telegram_webhook
```

Render shell orqali komanda ishlatish:

1. Render service ichiga kiring
2. `Shell` bo'limini oching
3. yuqoridagi komandalarni bajaring

Muhim eslatma:

- Render free web service uxlab qolishi mumkin, birinchi ochilish sekinroq bo'ladi
- SQLite Render free deployda doimiy saqlanishga kafolat bermaydi
- Admin paneldan upload qilingan rasmlar/video redeploydan keyin yo'qolishi mumkin
- Barqaror production uchun `DATABASE_URL` bilan Postgres va media uchun tashqi storage ishlatish yaxshi
- Hozirgi bepul variant demo va boshlang'ich savdo uchun yetadi, account rasmlarini URL orqali qo'yish eng xavfsiz

## Render Panelga Tayyor Kiritish

Quyidagilarni Render `Web Service` ichida aynan shu ko'rinishda kiriting.

### Root Directory

Bo'sh qoldiring.

### Build Command

```bash
bash build.sh
```

### Start Command

```bash
gunicorn --pythonpath backend config.wsgi:application
```

### Health Check Path

```text
/healthz
```

### Pre-Deploy Command

Bo'sh qoldiring, chunki migration `build.sh` ichida bor.

### Auto-Deploy

```text
On Commit
```

### Environment Variables

1-rasmdagi joyga quyidagilarni kiriting:

```env
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
DEBUG=False
PYTHON_VERSION=3.12.4
SECRET_KEY=<Render Generate tugmasi bilan yarating>
TELEGRAM_BOT_TOKEN=<BotFather bergan haqiqiy token>
TELEGRAM_BOT_USERNAME=sheikh_pbot
TELEGRAM_CONTACT_USERNAME=khVO1D
```

`DATABASE_URL` uchun 2 ta holat bor:

- agar Render Postgres ulasangiz: `DATABASE_URL=<Render Postgres Internal Database URL>`
- agar hozircha Postgres ishlatmasangiz: `DATABASE_URL` umuman qo'shmang yoki o'chirib tashlang

`SITE_URL` ni ham qo'shing:

```env
SITE_URL=https://your-service-name.onrender.com
```

Misol:

```env
SITE_URL=https://sheikh.onrender.com
```

Muhim:

- `SECRET_KEY` ni qo'lda yozmang, `Generate` tugmasi bilan yarating
- `TELEGRAM_BOT_USERNAME` ni `@` siz yozing
- `TELEGRAM_CONTACT_USERNAME` ni ham `@` siz yozing
- `DATABASE_URL` bo'sh string bo'lib turmasin, yo haqiqiy URL bo'lsin, yo umuman bo'lmasin

## Render Postgres Ochish

2-rasm, 3-rasm va 4-rasm uchun to'liq tartib:

1. Render dashboardda `New` -> `Postgres` bosing
2. `Name` maydoniga yozing:

```text
Sheikh
```

3. `Project` ixtiyoriy, hohlasangiz bo'sh qoldiring
4. `Database` maydonini bo'sh qoldirsangiz Render o'zi yaratadi
5. `User` maydonini bo'sh qoldirsangiz Render o'zi yaratadi
6. `Region` ni web service bilan bir xil qiling
7. `PostgreSQL Version` sifatida `18` qoldirsa bo'ladi
8. `Datadog API Key` bo'sh qolsin
9. `Datadog Region` o'zgartirmasa ham bo'ladi
10. `Storage` free uchun `1 GB`
11. `Storage Autoscaling` `Disabled`
12. `High Availability` `Disabled`
13. Pastdagi `Create Database` ni bosing

Database yaratilgandan keyin:

1. O'sha Postgres service ichiga kiring
2. `Info` yoki `Connect` bo'limidan `Internal Database URL` ni oling
3. Web Service -> `Environment` ga kiring
4. `DATABASE_URL` qo'shing
5. Value ichiga o'sha `Internal Database URL` ni qo'ying
6. `Save, rebuild, and deploy` bosing

## Render Deploydan Keyin

Deploy muvaffaqiyatli chiqqandan keyin:

1. Render service ichiga kiring
2. `Shell` bo'limini oching
3. Quyidagi komandalarni ishga tushiring

```bash
python manage.py createsuperuser
python manage.py set_telegram_webhook
```

Webhook uchun `SITE_URL` to'g'ri bo'lishi kerak. Masalan:

```env
SITE_URL=https://sheikh.onrender.com
```

Keyin Telegramda tekshiring:

```text
/start
```

## Render Xato Chiqsa

Agar quyidagi xato chiqsa:

```text
ValueError: No support for ''
```

Bu `DATABASE_URL` noto'g'ri yoki bo'sh ekanini bildiradi. Yechim:

- `DATABASE_URL` ni Render environment ichidan o'chiring
- yoki haqiqiy Render Postgres `Internal Database URL` qo'ying

Hozirgi loyiha kodi bo'sh yoki noto'g'ri `DATABASE_URL` bo'lsa SQLite'ga fallback qiladi, lekin Render panelda bo'sh qiymat qoldirmaslik baribir yaxshiroq.

## Environment Variables

Telegram savdo oqimi uchun asosiy qiymatlar:

- `SITE_URL`
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_BOT_USERNAME`
- `TELEGRAM_CONTACT_USERNAME`

Eski payment provider sozlamalari kerak bo'lsa, ular ham saqlangan:

- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `CLICK_SERVICE_ID`
- `CLICK_MERCHANT_ID`
- `CLICK_MERCHANT_USER_ID`
- `CLICK_SECRET_KEY`
- `PAYME_MERCHANT_ID`
- `PAYME_SECRET_KEY`

## Foydali komandalar

```bash
python manage.py check
python manage.py setup_demo
python manage.py runserver
python manage.py run_telegram_bot
python manage.py set_telegram_webhook
python manage.py collectstatic
.\start_all.bat
```
