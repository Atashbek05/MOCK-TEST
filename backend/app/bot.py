"""
Telegram bot — simple long-polling.

This file is the ONLY place the bot lives.
It runs in a background daemon thread started from main.py startup_event.

Why polling instead of webhook?
  Telegram sends updates to ONE destination — either a webhook URL or getUpdates.
  On Render free tier the server sleeps between requests, making webhook delivery
  unreliable. Polling works regardless: the thread asks Telegram for new messages
  every 30 seconds and processes them immediately.
"""

import os
import threading
import time
from typing import Optional

import requests

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN:   str = os.getenv("TELEGRAM_BOT_TOKEN", "")
APP_URL: str = os.getenv("FRONTEND_URL", "https://atashasd.vercel.app")
API:     str = f"https://api.telegram.org/bot{TOKEN}"


# ── Send a message ─────────────────────────────────────────────────────────────
def _send(chat_id: int, text: str, keyboard: Optional[dict] = None) -> None:
    payload: dict = {
        "chat_id":    chat_id,
        "text":       text,
        "parse_mode": "HTML",
    }
    if keyboard:
        payload["reply_markup"] = keyboard
    try:
        requests.post(f"{API}/sendMessage", json=payload, timeout=10)
    except Exception:
        pass  # never crash the thread on a send error


# ── Handle one Telegram update ────────────────────────────────────────────────
def _handle(update: dict) -> None:
    message = update.get("message", {})
    text    = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if not chat_id:
        return

    first_name = message.get("from", {}).get("first_name", "Student")

    if text.startswith("/start"):
        welcome = (
            f"👋 Hello, <b>{first_name}</b>!\n\n"
            "🎯 <b>IELTS Mock Test Platform</b>\n\n"
            "Practice Reading, Listening and Writing\n"
            "with AI-powered feedback.\n\n"
            "Tap the button below to open the platform 👇"
        )
        keyboard = {
            "inline_keyboard": [[
                {
                    "text":    "🚀 Open IELTS Platform",
                    "web_app": {"url": APP_URL},
                }
            ]]
        }
        _send(chat_id, welcome, keyboard)


# ── Polling loop (runs forever in a daemon thread) ────────────────────────────
def _poll() -> None:
    offset = 0
    while True:
        try:
            res = requests.get(
                f"{API}/getUpdates",
                params={"timeout": 30, "offset": offset},
                timeout=35,          # must be > Telegram timeout
            )
            data = res.json()
            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1   # acknowledge the update
                    _handle(update)
        except Exception:
            time.sleep(5)            # brief pause after any network error


# ── Public entry point — called once from main.py startup_event ───────────────
def start_polling() -> None:
    """
    1. Delete any registered webhook (required — polling and webhook are mutually exclusive).
    2. Start the polling loop in a daemon thread so it doesn't block the server.
    """
    if not TOKEN:
        return   # TELEGRAM_BOT_TOKEN not set — skip silently

    # Step 1: clear webhook so getUpdates starts receiving messages
    try:
        requests.post(
            f"{API}/deleteWebhook",
            json={"drop_pending_updates": True},
            timeout=10,
        )
    except Exception:
        pass

    # Step 2: daemon thread — dies automatically when the server process exits
    thread = threading.Thread(target=_poll, daemon=True, name="telegram-bot")
    thread.start()
