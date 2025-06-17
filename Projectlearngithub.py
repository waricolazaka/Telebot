import logging
import pyotp

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Ganti dengan token bot kamu
BOT_API_TOKEN = 'yourbottoken'  # <-- Ubah ini

# ====================== /start ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Saya adalah bot 2FA milik @alfinadia.\n"
        "Silakan kirim secret key 2FA Anda (16 karakter alfanumerik)."
    )

# Handler untuk menerima dan memproses secret key
async def otp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if all(c.isalnum() for c in user_input) and len(user_input) >= 16:
        try:
            totp = pyotp.TOTP(user_input)
            otp_code = totp.now()
            await update.message.reply_text(
                f"Kode OTP Anda adalah: <code>{otp_code}</code>",
                parse_mode='HTML'
            )
        except Exception as e:
            logging.error(f"Error saat generate OTP: {e}")
            await update.message.reply_text("Terjadi kesalahan saat menghasilkan OTP.")
    else:
        await update.message.reply_text("Mohon kirimkan secret key 2FA yang valid.")

# ============================= Main ============================================
def main():
    application = ApplicationBuilder().token(BOT_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, otp_handler))

    print("Bot jalan bang 🚀...")
    application.run_polling()

# ========================== Entry Point ========================================
if __name__ == '__main__':
    main()
