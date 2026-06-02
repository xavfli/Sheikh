@echo off
cd /d "%~dp0"

if not exist ".env" (
  echo .env fayl topilmadi.
  echo .env.example nusxasidan .env yarating va haqiqiy TELEGRAM_BOT_TOKEN yozing.
  pause
  exit /b 1
)

python manage.py run_telegram_bot
pause
