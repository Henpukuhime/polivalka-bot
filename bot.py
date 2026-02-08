import os
import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

plants = {}

REMIND_TEXTS = [
    "Кажется, {obj} может быть приятно попить 🌿",
    "{obj} по тебе соскучился 💚",
    "{obj} шлёт тебе «привет» 👋",
    "Полить {obj} — бесплатно, без регистрации и СМС",
    "У {obj} сегодня цвет настроения — зелёный",
]

scheduler = AsyncIOScheduler()


def resolve_name(data):
    return data.get("name") or "цветочек"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я Поливалка 🌱\n"
        "Я напоминаю о поливе — спокойно и без давления.\n\n"
        "Напиши /add чтобы добавить растение."
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Напиши так:\n"
        "`Имя растения; интервал в днях`\n\n"
        "Например:\n"
        "`Жорик; 7`",
        parse_mode="Markdown"
    )


async def save_plant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ";" not in update.message.text:
        return

    name, days = update.message.text.split(";")
    name = name.strip()
    days = int(days.strip())

    chat_id = update.message.chat_id
    plants[chat_id] = {
        "name": name,
        "interval": days,
        "next": datetime.now() + timedelta(days=days),
    }

    scheduler.add_job(
        send_reminder,
        "date",
        run_date=plants[chat_id]["next"],
        args=[context, chat_id],
    )

    await update.message.reply_text(
        f"Готово 🌿 Я буду напоминать про {name}"
    )


async def send_reminder(context, chat_id):
    data = plants.get(chat_id)
    if not data:
        return

    name = resolve_name(data)
    text = REMIND_TEXTS[datetime.now().second % len(REMIND_TEXTS)].format(obj=name)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Пора полить", callback_data="water"),
            InlineKeyboardButton("Не сегодня", callback_data="later"),
        ]
    ])

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = plants.get(chat_id)

    if not data:
        return

    if query.data == "water":
        data["next"] = datetime.now() + timedelta(days=data["interval"])
        scheduler.add_job(
            send_reminder,
            "date",
            run_date=data["next"],
            args=[context, chat_id],
        )
        await query.edit_message_text("Записала 💧 Пусть пьёт 🌿")

    elif query.data == "later":
        data["next"] = datetime.now() + timedelta(days=1)
        scheduler.add_job(
            send_reminder,
            "date",
            run_date=data["next"],
            args=[context, chat_id],
        )
        await query.edit_message_text("Окей. Вернусь завтра")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("save", save_plant))
    app.add_handler(CallbackQueryHandler(button))

    scheduler.start()
    app.run_polling()


if __name__ == "__main__":
    main()
