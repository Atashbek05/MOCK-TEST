"""
Telegram bot — simple long-polling.

This file is the ONLY place the bot lives.
It runs in a background daemon thread started from main.py startup_event.

Why polling instead of webhook?
  Telegram sends updates to ONE destination — either a webhook URL or getUpdates.
  On Render free tier the server sleeps between requests, making webhook delivery
  unreliable. Polling works regardless: the thread asks Telegram for new messages
  every 30 seconds and processes them immediately.

Phase 7 additions:
  - /progress  — user's band stats from DB
  - /latestscore — single latest test result from DB
  - /starttest — opens Mini App to take a test
  - /dashboard — opens Mini App dashboard
  - Daily reminder system for inactive students
"""

import os
import threading
import time
from datetime import datetime, timedelta
from typing import Optional

import requests

from . import models
from .database import SessionLocal

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN:   str = os.getenv("TELEGRAM_BOT_TOKEN", "")
APP_URL: str = os.getenv("FRONTEND_URL", "https://atashasd.vercel.app")
API:     str = f"https://api.telegram.org/bot{TOKEN}"


# ── Send a message ─────────────────────────────────────────────────────────────
def _send(chat_id: int, text: str, keyboard: Optional[dict] = None,
          parse_mode: str = "Markdown") -> None:
    payload: dict = {
        "chat_id":    chat_id,
        "text":       text,
        "parse_mode": parse_mode,
    }
    if keyboard:
        payload["reply_markup"] = keyboard
    try:
        requests.post(f"{API}/sendMessage", json=payload, timeout=10)
    except Exception:
        pass


# ── Bot command handlers ───────────────────────────────────────────────────────

def _cmd_start(chat_id: int, first_name: str) -> None:
    welcome = (
        f"👋 Hello, <b>{first_name}</b>!\n\n"
        "🎯 <b>IELTS Mock Test Platform</b>\n\n"
        "Practice Reading, Listening and Writing\n"
        "with AI-powered feedback.\n\n"
        "📌 <b>Commands:</b>\n"
        "/progress — Your stats\n"
        "/latestscore — Last test result\n"
        "/starttest — Open a test\n"
        "/dashboard — Your dashboard\n\n"
        "Tap the button below to open the platform 👇"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "🚀 Open IELTS Platform", "web_app": {"url": f"{APP_URL}/tg-app.html"}}],
            [{"text": "🔗 Link Account", "url": f"{APP_URL}/telegram-connect.html"}],
        ]
    }
    try:
        requests.post(f"{API}/sendMessage", json={
            "chat_id": chat_id, "text": welcome,
            "parse_mode": "HTML", "reply_markup": keyboard,
        }, timeout=10)
    except Exception:
        pass


def _cmd_help(chat_id: int) -> None:
    _send(chat_id, (
        "📚 *Commands:*\n\n"
        "/start — Main menu\n"
        "/help — This list\n"
        "/progress — Your band stats\n"
        "/latestscore — Latest test result\n"
        "/starttest — Open a test in Mini App\n"
        "/dashboard — Open your dashboard\n"
        "/link — Link Telegram to your account\n"
        "/status — Check account link status"
    ))


def _cmd_link(chat_id: int) -> None:
    """No code provided — show instructions on how to get a code from the website."""
    keyboard = {"inline_keyboard": [[
        {"text": "🔗 Get Verification Code", "url": f"{APP_URL}/telegram-connect.html"}
    ]]}
    _send(chat_id, (
        "To link your Telegram with your IELTS account:\n\n"
        "1️⃣ Open the platform and go to *Telegram Connect*\n"
        "2️⃣ Get your 6-digit verification code\n"
        "3️⃣ Send it here: `/link 123456`\n\n"
        "Tap the button to get your code 👇"
    ), keyboard)


def _cmd_link_code(chat_id: int, tg_id: int, code: str,
                   tg_username: Optional[str]) -> None:
    """
    User sent /link 123456 — verify the code in DB and link their account.
    Security checks:
      • code must exist and be unused
      • code must not be expired (10-minute window)
      • this Telegram ID must not already be linked to a different account
    """
    db = SessionLocal()
    try:
        vc = (db.query(models.TelegramVerificationCode)
              .filter(models.TelegramVerificationCode.code == code)
              .first())

        if not vc:
            _send(chat_id, "❌ Invalid code. Generate a new one on the platform.")
            return

        if vc.used:
            _send(chat_id, "❌ This code was already used. Generate a new one.")
            return

        # Compare expiry — DB stores naive UTC; handle both cases
        expires = vc.expires_at
        if expires.tzinfo is not None:
            expires = expires.replace(tzinfo=None)
        if datetime.utcnow() > expires:
            _send(chat_id, "❌ Code expired (10-minute limit). Generate a new one.")
            return

        # Conflict: this Telegram account linked to a *different* platform account
        conflict = (db.query(models.User)
                    .filter(models.User.telegram_id == tg_id,
                            models.User.id != vc.user_id)
                    .first())
        if conflict:
            _send(chat_id,
                  "❌ This Telegram is already linked to a different account.\n"
                  "Unlink it first from that account.")
            return

        user = db.query(models.User).filter(models.User.id == vc.user_id).first()
        if not user:
            _send(chat_id, "❌ Account not found. Please try again.")
            return

        # All good — link!
        user.telegram_id       = tg_id
        user.telegram_username = tg_username
        vc.used                = True
        db.commit()

        keyboard = {"inline_keyboard": [[
            {"text": "🚀 Open Dashboard", "url": f"{APP_URL}/dashboard.html"}
        ]]}
        _send(chat_id, (
            f"✅ *Successfully linked!*\n\n"
            f"Account: *{user.name}* ({user.email})\n\n"
            f"You'll now receive:\n"
            f"• 📊 Test results after each submission\n"
            f"• ⏰ Study reminders\n"
            f"• 📢 Teacher announcements\n"
        ), keyboard)
    finally:
        db.close()


def _cmd_status(chat_id: int, tg_id: int) -> None:
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if user:
            _send(chat_id, f"✅ Linked to account *{user.name}* ({user.email})")
        else:
            _send(chat_id, "❌ Not linked yet. Use /link to connect your account.")
    finally:
        db.close()


def _cmd_progress(chat_id: int, tg_id: int) -> None:
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if not user:
            _send(chat_id, "❌ Account not linked. Use /link first.")
            return

        results = (db.query(models.TeacherTestResult)
                   .filter(models.TeacherTestResult.student_id == user.id)
                   .order_by(models.TeacherTestResult.created_at.desc())
                   .limit(10).all())
        writing = (db.query(models.WritingResult)
                   .filter(models.WritingResult.user_id == user.id)
                   .order_by(models.WritingResult.created_at.desc())
                   .first())

        if not results and not writing:
            _send(chat_id, "📊 No results yet.\n\nStart a test: /starttest")
            return

        text = f"📊 *Progress — {user.name}*\n\n"
        if results:
            bands = [r.band for r in results]
            text += f"🎯 Best band: *{max(bands)}*\n"
            text += f"📈 Average: *{round(sum(bands)/len(bands), 1)}*\n"
            text += f"📝 Attempts: *{len(results)}*\n"
        if writing:
            text += f"\n✏️ Last Writing: *{writing.band_score}* band\n"
        text += f"\n[Open Dashboard]({APP_URL}/tg-app.html)"
        _send(chat_id, text)
    finally:
        db.close()


def _cmd_latestscore(chat_id: int, tg_id: int) -> None:
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if not user:
            _send(chat_id, "❌ Account not linked. Use /link first.")
            return

        r = (db.query(models.TeacherTestResult)
             .filter(models.TeacherTestResult.student_id == user.id)
             .order_by(models.TeacherTestResult.created_at.desc())
             .first())
        if not r:
            _send(chat_id, "❌ No results yet. Take a test: /starttest")
            return

        test = db.query(models.TeacherTest).filter(models.TeacherTest.id == r.test_id).first()
        test_name = test.title if test else f"Test #{r.test_id}"
        _send(chat_id, (
            f"🏆 *Latest Result*\n\n"
            f"📝 {test_name}\n"
            f"🎯 Band: *{r.band}*\n"
            f"✔️ {r.correct}/{r.total} correct\n"
            f"📅 {r.created_at.strftime('%d.%m.%Y')}\n\n"
            f"[View all results]({APP_URL}/tg-app.html)"
        ))
    finally:
        db.close()


def _cmd_open_app(chat_id: int, command: str) -> None:
    label = "📊 My Dashboard" if command == "/dashboard" else "🚀 Start Test"
    keyboard = {"inline_keyboard": [[
        {"text": label, "web_app": {"url": f"{APP_URL}/tg-app.html"}}
    ]]}
    _send(chat_id, "Opening the platform...", keyboard)


# ── Daily reminders for inactive students ─────────────────────────────────────

def _send_daily_reminders() -> None:
    """
    Find students with linked Telegram accounts who have NOT submitted any test
    in the last 3 days, and send them a friendly nudge.

    Called once per UTC day from the polling loop.
    Note: on Render free tier the server may sleep, so reminders are best-effort.
    """
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=3)
        students = (db.query(models.User)
                    .filter(models.User.telegram_id.isnot(None),
                            models.User.role == "student")
                    .all())
        for user in students:
            latest = (db.query(models.TeacherTestResult)
                      .filter(models.TeacherTestResult.student_id == user.id)
                      .order_by(models.TeacherTestResult.created_at.desc())
                      .first())
            # Normalize to naive UTC for comparison
            if latest:
                lat = latest.created_at
                if lat.tzinfo:
                    lat = lat.replace(tzinfo=None)
                if lat >= cutoff:
                    continue  # active recently — skip
            # Send reminder
            keyboard = {"inline_keyboard": [[
                {"text": "📖 Take a Test", "web_app": {"url": f"{APP_URL}/tg-app.html"}}
            ]]}
            _send(user.telegram_id, (
                "⏰ *Reminder!*\n\n"
                "You haven't taken a test in 3+ days.\n"
                "Consistent practice is the key to IELTS success! 💪"
            ), keyboard)
    except Exception:
        pass
    finally:
        db.close()


# ── Handle one Telegram update ────────────────────────────────────────────────
def _handle(update: dict) -> None:
    message  = update.get("message", {})
    text     = message.get("text", "")
    chat_id  = message.get("chat", {}).get("id")
    from_obj = message.get("from", {})

    if not chat_id:
        return

    first_name = from_obj.get("first_name", "Student")
    tg_id      = from_obj.get("id")

    if text.startswith("/start"):
        _cmd_start(chat_id, first_name)
    elif text == "/help":
        _cmd_help(chat_id)
    elif text.startswith("/link"):
        # /link       → show instructions
        # /link 123456 → verify code and link account
        parts = text.split()
        if (len(parts) == 2 and parts[1].isdigit()
                and len(parts[1]) == 6 and tg_id):
            _cmd_link_code(chat_id, tg_id, parts[1], from_obj.get("username"))
        else:
            _cmd_link(chat_id)
    elif text == "/status" and tg_id:
        _cmd_status(chat_id, tg_id)
    elif text == "/progress" and tg_id:
        _cmd_progress(chat_id, tg_id)
    elif text == "/latestscore" and tg_id:
        _cmd_latestscore(chat_id, tg_id)
    elif text in ("/starttest", "/dashboard"):
        _cmd_open_app(chat_id, text)


# ── Polling loop (runs forever in a daemon thread) ────────────────────────────
def _poll() -> None:
    offset = 0
    last_reminder_day: Optional[int] = None

    while True:
        # ── Long-poll Telegram for new updates ────────────────────────────────
        try:
            res = requests.get(
                f"{API}/getUpdates",
                params={"timeout": 30, "offset": offset},
                timeout=35,
            )
            data = res.json()
            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    _handle(update)
        except Exception:
            time.sleep(5)

        # ── Daily reminders: fire once per UTC calendar day ───────────────────
        today = time.gmtime().tm_yday
        if today != last_reminder_day:
            last_reminder_day = today
            threading.Thread(target=_send_daily_reminders, daemon=True,
                             name="tg-reminders").start()


# ── Public entry point — called once from main.py startup_event ───────────────
def start_polling() -> None:
    """
    1. Delete any registered webhook (required — polling and webhook are mutually exclusive).
    2. Start the polling loop in a daemon thread so it doesn't block the server.
    """
    if not TOKEN:
        return   # TELEGRAM_BOT_TOKEN not set — skip silently

    try:
        requests.post(
            f"{API}/deleteWebhook",
            json={"drop_pending_updates": True},
            timeout=10,
        )
    except Exception:
        pass

    thread = threading.Thread(target=_poll, daemon=True, name="telegram-bot")
    thread.start()
