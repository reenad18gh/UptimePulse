import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "UptimePulse")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Riyadh")

CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "30"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "3"))

HTTP_TARGETS = [
    x.strip()
    for x in os.getenv("HTTP_TARGETS", "https://example.com").split(",")
    if x.strip()
]

TCP_TARGETS = [
    x.strip()
    for x in os.getenv("TCP_TARGETS", "").split(",")
    if x.strip()
]

ENABLE_TELEGRAM = os.getenv("ENABLE_TELEGRAM", "false").lower() in {"true", "1", "yes", "y", "on"}
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
