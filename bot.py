# Bot is alive ✅ 2026-02-08
import os
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Привет! Я Поливалка.\n"
        "Буду напоминать тебе поливать растения 💧"
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я жива 🌱")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Что ты хочешь добавить?\n\n"
        "🌱 Одно растение\n"
        "🌿 Группу растений\n\n"
        "Пока просто ответь текстом: растение или группа"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("add", add))

    print("🌱 Polivalka started")

    # ВАЖНО: без await, без asyncio.run
    app.run_polling()


if __name__ == "__main__":
    main()
