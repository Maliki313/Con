"""
Enhanced Telegram Bot with OpenAI Integration
Fixed version with proper error handling, logging, and modern OpenAI API usage.
"""

import telebot
from openai import OpenAI
import os
import logging
import time
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramOpenAIBot:
    """Enhanced Telegram bot with OpenAI Assistant integration."""
    
    def __init__(self):
        """Initialize bot with environment variables."""
        self.telegram_token = os.environ.get("TELEGRAM_TOKEN")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.assistant_id = os.environ.get("ASSISTANT_ID")
        
        if not all([self.telegram_token, self.openai_api_key, self.assistant_id]):
            raise ValueError("Missing required environment variables")
        
        # Initialize clients
        self.bot = telebot.TeleBot(self.telegram_token)
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Setup message handlers
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup message handlers."""
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.handle_start(message)
            
        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            self.handle_help(message)
            
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            self.handle_message(message)
    
    def handle_start(self, message):
        """Handle /start command."""
        welcome_text = """مرحباً بك في البوت الذكي!
        
أرسل لي أي رسالة وسأقوم بالرد عليك باستخدام الذكاء الاصطناعي.

الأوامر المتاحة:
/start - بدء المحادثة
/help - عرض المساعدة"""
        
        self.bot.reply_to(message, welcome_text)
    
    def handle_help(self, message):
        """Handle /help command."""
        help_text = """المساعدة:

هذا البوت يستخدم مساعد OpenAI للرد على رسائلك.
ببساطة أرسل أي رسالة وستحصل على رد ذكي.

إذا واجهت أي مشاكل، تأكد من إعداد المتغيرات البيئية بشكل صحيح."""
        
        self.bot.reply_to(message, help_text)
    
    def handle_message(self, message):
        """Handle regular messages with OpenAI Assistant."""
        user_id = message.from_user.id
        user_input = message.text
        
        logger.info(f"Processing message from user {user_id}: {user_input[:50]}...")
        
        try:
            # Send "typing" status
            self.bot.send_chat_action(message.chat.id, 'typing')
            
            # Create thread and get response
            response = self.get_ai_response(user_input)
            
            if response:
                self.bot.reply_to(message, response)
            else:
                self.bot.reply_to(message, "عذراً، لم أتمكن من معالجة طلبك. حاول مرة أخرى.")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            error_message = "حدث خطأ أثناء معالجة رسالتك. يرجى المحاولة مرة أخرى لاحقاً."
            self.bot.reply_to(message, error_message)
    
    def get_ai_response(self, user_input: str) -> Optional[str]:
        """Get response from OpenAI Assistant."""
        try:
            # Create a new thread
            thread = self.client.beta.threads.create()
            
            # Add message to thread
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )
            
            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant_id
            )
            
            # Wait for completion with timeout
            max_wait_time = 30  # seconds
            wait_time = 0
            
            while wait_time < max_wait_time:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                
                if run_status.status == "completed":
                    break
                elif run_status.status == "failed":
                    logger.error(f"Assistant run failed: {run_status.last_error}")
                    return None
                    
                time.sleep(1)
                wait_time += 1
            
            if wait_time >= max_wait_time:
                logger.error("Assistant response timeout")
                return None
            
            # Get the response
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            
            if messages.data:
                response = messages.data[0].content[0].text.value
                return response
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return None
    
    def run(self):
        """Start the bot."""
        logger.info("Starting Telegram bot...")
        try:
            self.bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            logger.error(f"Bot polling error: {e}")
            raise

def main():
    """Main function."""
    try:
        bot = TelegramOpenAIBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()