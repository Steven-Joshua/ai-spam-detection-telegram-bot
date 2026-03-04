import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 🔐 Load token from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in environment variables.")

# 🔗 FastAPI Backend URL
FASTAPI_URL = "http://127.0.0.1:8000/analyze"


# 🔹 Format Final Message
def format_response(verdict, confidence, analysis):

    warning = ""
    if confidence != "N/A":
        try:
            if float(confidence) < 60:
                warning = "\n⚠️ *This message is borderline. Please verify manually.*\n"
        except:
            pass

    return f"""
🛡️ *Spam Detection Result:* {verdict.upper()}
📊 *Confidence:* {confidence}%

{warning}
{analysis}
"""


# 🛡️ Handle Text Messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = requests.post(
            FASTAPI_URL,
            data={"text": user_text},  # Form-data
            timeout=30
        )

        data = response.json()

        verdict = data.get("verdict", "Unknown")
        confidence = data.get("confidence", "N/A")
        analysis = data.get("safety_analysis", "No explanation generated.")

    except Exception:
        verdict = "Error"
        confidence = "N/A"
        analysis = "⚠️ Could not connect to backend service."

    final_message = format_response(verdict, confidence, analysis)

    await update.message.reply_text(final_message, parse_mode="Markdown")


# 🖼️ Handle Image Messages
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]  # Highest resolution
        file = await photo.get_file()

        image_path = "telegram_temp.jpg"
        await file.download_to_drive(image_path)

        with open(image_path, "rb") as img:
            response = requests.post(
                FASTAPI_URL,
                files={"file": img},   # Make sure FastAPI expects 'file'
                timeout=60
            )

        os.remove(image_path)

        data = response.json()

        verdict = data.get("verdict", "Unknown")
        confidence = data.get("confidence", "N/A")
        analysis = data.get("safety_analysis", "No explanation generated.")

    except Exception:
        verdict = "Error"
        confidence = "N/A"
        analysis = "⚠️ Failed to process image."

    final_message = format_response(verdict, confidence, analysis)

    await update.message.reply_text(final_message, parse_mode="Markdown")


# 🚀 Start Bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Text handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Image handler
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("🤖 Telegram Spam Bot Running...")
    app.run_polling()