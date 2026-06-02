@echo off
cd /d "%~dp0"

if not exist ".env" (
  echo .env fayl topilmadi.
  echo .env.example nusxasidan .env yarating va haqiqiy TELEGRAM_BOT_TOKEN yozing.
  pause
  exit /b 1
)

start "Sheikh Website" cmd /k "cd /d %~dp0 && python manage.py runserver"
start "Sheikh Telegram Bot" cmd /k "cd /d %~dp0 && python manage.py run_telegram_bot"
