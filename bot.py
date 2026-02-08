# Bot is alive ✅ 2026-02-08
import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
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
    keyboard = [
        [
            InlineKeyboardButton("🌱 Растение", callback_data="add_plant"),
            InlineKeyboardButton("🌿 Группа растений", callback_data="add_group"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Что ты хочешь добавить?",
        reply_markup=reply_markup,
    )


async def add_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "add_plant":
        text = (
            "🌱 Хорошо.\n\n"
            "Напиши, что это за растение.\n"
            "Если у него есть имя — тоже напиши."
        )
    elif query.data == "add_group":
        text = (
            "🌿 Хорошо.\n\n"
            "Напиши, что это за группа растений.\n"
            "Можно указать общее имя группы."
        )
    else:
        return

    await query.message.reply_text(text)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("add", add))

    app.add_handler(CallbackQueryHandler(add_choice))

    print("🌱 Polivalka started")

    app.run_polling()


if __name__ == "__main__":
    main()
