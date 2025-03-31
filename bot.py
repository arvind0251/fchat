import http.client
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 🔹 Telegram Bot Token & API Details
TELEGRAM_BOT_TOKEN = "7810505308:AAGr-fIzBSy-WXYuCZlH-fvGbCdDhRtuRLI"
RAPIDAPI_KEY = "c02f3ddea8msh041875afb61cf38p1a5668jsn39030ba4fd0c"
RAPIDAPI_HOST = "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com"

# 🔹 Logging Setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🔹 Function: Get Response from GPT-4 API
def get_ai_response(user_message):
    try:
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
        
        response_json = json.loads(data.decode("utf-8"))

        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "😞 AI se response nahi mila, thodi der baad try karein!"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# 🔹 Function: Handle /start Command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 Hello! Main ek AI chatbot hoon. Mujhse kuch bhi poochho!")

# 🔹 Function: Handle User Messages
async def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    ai_reply = get_ai_response(user_message)
    await update.message.reply_text(ai_reply)

# 🔹 Main Function to Run the Bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 AI Telegram Bot is Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
