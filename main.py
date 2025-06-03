import telebot
import openai
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ORG_ID = os.environ.get("ORG_ID")
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY
openai.organization = ORG_ID

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    try:
        thread = openai.beta.threads.create()
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )
        result = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        reply = f"نهج المنتقم يجاوبك: {result.status}"
    except Exception as e:
        reply = f"حدث خطأ: {e}"
    
    bot.reply_to(message, reply)

bot.polling()