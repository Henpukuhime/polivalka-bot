import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ---------- ЛОГИ ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- TOKEN ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment variables")

# ---------- HANDLERS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌱 Добавить растение", callback_data="add_plant")],
        [InlineKeyboardButton("💧 Полить сегодня", callback_data="water_now")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет 🌿\n\n"
        "Я Поливалка — помогу не забыть полить твои растения.\n"
        "Выбирай, что делаем:",
        reply_markup=reply_markup,
    )


# ---------- MAIN ----------
def main():
    app: Application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    logger.info("🌱 Polivalka started")

    app.run_polling()


if __name__ == "__main__":
    main()
