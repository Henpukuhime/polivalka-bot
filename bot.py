import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ---------- НАСТРОЙКИ ----------

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment variables")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ---------- КНОПКИ ----------

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["Пора полить 🌿"],
        ["Не сегодня", "Отложить"],
    ],
    resize_keyboard=True,
)

# ---------- ХЭНДЛЕРЫ ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Поливалка 🌱\n\n"
        "Я буду помогать тебе помнить о поливе растений.\n"
        "Без давления. Без занудства.\n\n"
        "Начнём?",
        reply_markup=MAIN_KEYBOARD,
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я пока этого не умею, но я стараюсь 🌿"
    )

# ---------- ЗАПУСК ----------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))

    app.add_handler(CommandHandler(None, unknown))

    print("🌱 Polivalka started")
    app.run_polling()


if __name__ == "__main__":
    main()
