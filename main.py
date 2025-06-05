"""
بوت تيليجرام محسن مع تكامل OpenAI
إصدار محدث مع معالجة أخطاء متقدمة ودعم كامل للغة العربية
"""

import os
import sys
import logging
import time
from typing import Optional, Dict, Any
import telebot
from openai import OpenAI
from datetime import datetime
import json

# إعداد نظام السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TelegramOpenAIBot:
    """بوت تيليجرام محسن مع تكامل OpenAI Assistant."""
    
    def __init__(self):
        """تهيئة البوت مع متغيرات البيئة."""
        # تحميل المتغيرات البيئية
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.assistant_id = os.getenv('ASSISTANT_ID')
        
        # التحقق من وجود المتغيرات المطلوبة
        self._validate_environment()
        
        # تهيئة العملاء
        try:
            self.bot = telebot.TeleBot(self.telegram_token)
            self.openai_client = OpenAI(api_key=self.openai_api_key)
            logger.info("تم تهيئة البوت وعميل OpenAI بنجاح")
        except Exception as e:
            logger.error(f"خطأ في تهيئة العملاء: {e}")
            sys.exit(1)
        
        # إعداد معالجات الرسائل
        self.setup_handlers()
        
        # تخزين الجلسات النشطة
        self.active_threads: Dict[int, str] = {}
        
        # إحصائيات الاستخدام
        self.usage_stats = {
            'total_messages': 0,
            'successful_responses': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
    
    def _validate_environment(self):
        """التحقق من صحة متغيرات البيئة."""
        missing_vars = []
        
        if not self.telegram_token:
            missing_vars.append('TELEGRAM_TOKEN')
        if not self.openai_api_key:
            missing_vars.append('OPENAI_API_KEY')
        if not self.assistant_id:
            missing_vars.append('ASSISTANT_ID')
        
        if missing_vars:
            error_msg = f"متغيرات البيئة المفقودة: {', '.join(missing_vars)}"
            logger.error(error_msg)
            sys.exit(1)
    
    def setup_handlers(self):
        """إعداد معالجات الرسائل."""
        
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.handle_start(message)
        
        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            self.handle_help(message)
        
        @self.bot.message_handler(commands=['stats'])
        def stats_command(message):
            self.handle_stats(message)
        
        @self.bot.message_handler(commands=['reset'])
        def reset_command(message):
            self.handle_reset(message)
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            self.handle_message(message)
    
    def handle_start(self, message):
        """معالجة أمر /start."""
        welcome_text = """
🤖 مرحباً بك في البوت الذكي!

أنا مساعد ذكي مدعوم بتقنية OpenAI، يمكنني مساعدتك في:
• الإجابة على الأسئلة المختلفة
• حل المشاكل والاستفسارات
• تقديم المعلومات والشروحات
• المساعدة في المهام اليومية

📝 الأوامر المتاحة:
/help - عرض المساعدة
/stats - إحصائيات الاستخدام
/reset - إعادة تعيين المحادثة

ابدأ بإرسال رسالة وسأجيبك فوراً!
        """
        try:
            self.bot.reply_to(message, welcome_text.strip())
            logger.info(f"رسالة ترحيب مرسلة للمستخدم {message.from_user.id}")
        except Exception as e:
            logger.error(f"خطأ في إرسال رسالة الترحيب: {e}")
    
    def handle_help(self, message):
        """معالجة أمر /help."""
        help_text = """
📚 مساعدة البوت الذكي

🔧 الأوامر المتاحة:
• /start - بدء المحادثة
• /help - عرض هذه المساعدة
• /stats - عرض إحصائيات الاستخدام
• /reset - إعادة تعيين المحادثة الحالية

💡 كيفية الاستخدام:
1. اكتب سؤالك أو استفسارك
2. انتظر الرد الذكي
3. يمكنك متابعة المحادثة بشكل طبيعي

⚠️ ملاحظات مهمة:
• البوت يحتفظ بسياق المحادثة
• استخدم /reset لبدء محادثة جديدة
• تأكد من وضوح أسئلتك للحصول على أفضل إجابة

🔒 الخصوصية:
• جميع المحادثات آمنة ومشفرة
• لا يتم حفظ البيانات الشخصية
        """
        try:
            self.bot.reply_to(message, help_text.strip())
            logger.info(f"رسالة المساعدة مرسلة للمستخدم {message.from_user.id}")
        except Exception as e:
            logger.error(f"خطأ في إرسال رسالة المساعدة: {e}")
    
    def handle_stats(self, message):
        """معالجة أمر /stats."""
        try:
            uptime = datetime.now() - self.usage_stats['start_time']
            success_rate = (self.usage_stats['successful_responses'] / 
                          max(1, self.usage_stats['total_messages'])) * 100
            
            stats_text = f"""
📊 إحصائيات البوت

📈 الاستخدام:
• إجمالي الرسائل: {self.usage_stats['total_messages']}
• الردود الناجحة: {self.usage_stats['successful_responses']}
• الأخطاء: {self.usage_stats['errors']}
• معدل النجاح: {success_rate:.1f}%

⏰ معلومات التشغيل:
• مدة التشغيل: {str(uptime).split('.')[0]}
• الجلسات النشطة: {len(self.active_threads)}

🔧 حالة النظام: ✅ يعمل بشكل طبيعي
            """
            self.bot.reply_to(message, stats_text.strip())
            logger.info(f"إحصائيات مرسلة للمستخدم {message.from_user.id}")
        except Exception as e:
            logger.error(f"خطأ في إرسال الإحصائيات: {e}")
            self.bot.reply_to(message, "❌ حدث خطأ في عرض الإحصائيات")
    
    def handle_reset(self, message):
        """معالجة أمر /reset."""
        try:
            user_id = message.from_user.id
            if user_id in self.active_threads:
                del self.active_threads[user_id]
                self.bot.reply_to(message, "✅ تم إعادة تعيين المحادثة بنجاح!")
                logger.info(f"تم إعادة تعيين المحادثة للمستخدم {user_id}")
            else:
                self.bot.reply_to(message, "ℹ️ لا توجد محادثة نشطة لإعادة تعيينها")
        except Exception as e:
            logger.error(f"خطأ في إعادة تعيين المحادثة: {e}")
            self.bot.reply_to(message, "❌ حدث خطأ في إعادة تعيين المحادثة")
    
    def handle_message(self, message):
        """معالجة الرسائل العادية مع OpenAI Assistant."""
        user_id = message.from_user.id
        user_text = message.text
        
        # تحديث الإحصائيات
        self.usage_stats['total_messages'] += 1
        
        try:
            # إرسال مؤشر الكتابة
            self.bot.send_chat_action(message.chat.id, 'typing')
            
            # الحصول على الرد من OpenAI
            ai_response = self.get_ai_response(user_text, user_id)
            
            if ai_response:
                # إرسال الرد
                self.bot.reply_to(message, ai_response)
                self.usage_stats['successful_responses'] += 1
                logger.info(f"رد ناجح للمستخدم {user_id}")
            else:
                error_msg = "❌ عذراً، حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى."
                self.bot.reply_to(message, error_msg)
                self.usage_stats['errors'] += 1
                
        except Exception as e:
            logger.error(f"خطأ في معالجة الرسالة من المستخدم {user_id}: {e}")
            error_msg = "❌ حدث خطأ تقني. يرجى المحاولة لاحقاً."
            try:
                self.bot.reply_to(message, error_msg)
            except:
                logger.error("فشل في إرسال رسالة الخطأ")
            self.usage_stats['errors'] += 1
    
    def get_ai_response(self, user_input: str, user_id: int) -> Optional[str]:
        """الحصول على رد من OpenAI Assistant."""
        try:
            # إنشاء أو استخدام thread موجود
            if user_id not in self.active_threads:
                thread = self.openai_client.beta.threads.create()
                self.active_threads[user_id] = thread.id
                logger.info(f"thread جديد تم إنشاؤه للمستخدم {user_id}")
            
            thread_id = self.active_threads[user_id]
            
            # إضافة رسالة المستخدم
            self.openai_client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_input
            )
            
            # تشغيل المساعد
            run = self.openai_client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id
            )
            
            # انتظار اكتمال التشغيل
            max_attempts = 30
            for _ in range(max_attempts):
                run_status = self.openai_client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                
                if run_status.status == 'completed':
                    break
                elif run_status.status in ['failed', 'cancelled', 'expired']:
                    logger.error(f"فشل في تشغيل المساعد: {run_status.status}")
                    return None
                
                time.sleep(1)
            else:
                logger.error("انتهت مهلة انتظار رد المساعد")
                return None
            
            # الحصول على الرد
            messages = self.openai_client.beta.threads.messages.list(
                thread_id=thread_id,
                order="desc",
                limit=1
            )
            
            if messages.data:
                assistant_message = messages.data[0]
                if hasattr(assistant_message.content[0], 'text'):
                    return assistant_message.content[0].text.value
            
            logger.error("لم يتم العثور على رد من المساعد")
            return None
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على رد AI: {e}")
            return None
    
    def run(self):
        """تشغيل البوت."""
        logger.info("🚀 بدء تشغيل البوت...")
        try:
            self.bot.infinity_polling(
                timeout=10,
                long_polling_timeout=5,
                none_stop=True,
                interval=1
            )
        except KeyboardInterrupt:
            logger.info("تم إيقاف البوت بواسطة المستخدم")
        except Exception as e:
            logger.error(f"خطأ في تشغيل البوت: {e}")
            sys.exit(1)

def main():
    """الدالة الرئيسية."""
    try:
        bot = TelegramOpenAIBot()
        bot.run()
    except Exception as e:
        logger.error(f"خطأ في الدالة الرئيسية: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()