import telebot
import openai
import os

# المتغيرات البيئية
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ORG_ID = os.environ.get("ORG_ID")
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")

# إعداد البوت
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

        # ننتظر انتهاء تشغيل المساعد
        import time
        status = ""
        while True:
            status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if status.status == "completed":
                break
            time.sleep(1)

        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        reply = messages.data[0].content[0].text.value

    except Exception as e:
        reply = f"حدث خطأ: {e}"

    bot.reply_to(message, reply)

bot.polling()
