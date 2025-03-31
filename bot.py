import http.client
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# RapidAPI aur Telegram API keys
TELEGRAM_BOT_TOKEN = "7810505308:AAGr-fIzBSy-WXYuCZlH-fvGbCdDhRtuRLI"
RAPIDAPI_KEY = "823ad731bemsh1a89f7cbcabd094p1f2447jsnad1907e6f3a1"
RAPIDAPI_HOST = "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com"

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# GPT-4o API se response lene ka function
def get_ai_response(user_message):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    payload = json.dumps({
        "messages": [{"role": "user", "content": user_message}],
        "model": "gpt-4o",
        "max_tokens": 100,
        "temperature": 0.9
    })
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    try:
        response_json = json.loads(data)
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        return "Sorry, AI response nahi mil saka!"

# Start command ka function
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! Main ek AI chatbot hoon. Mujhse kuch bhi poochho!")

# AI response ka function
async def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    ai_reply = get_ai_response(user_message)
    await update.message.reply_text(ai_reply)

# Main function
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 AI Telegram Bot is Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
