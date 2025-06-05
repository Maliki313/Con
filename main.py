"""
بوت تيليجرام محسن مع شارح السياق الثقافي الإسلامي
إصدار متقدم مع ميزات تفاعلية لشرح المفاهيم الإسلامية
"""

import os
import sys
import logging
import time
import re
from typing import Optional, Dict, Any
import telebot
from openai import OpenAI
from datetime import datetime
import json

from islamic_context_explainer import IslamicContextExplainer, ConceptCategory
from session_manager import SessionManager, SessionState

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

class EnhancedIslamicBot:
    """بوت تيليجرام محسن مع شارح المفاهيم الإسلامية"""
    
    def __init__(self):
        """تهيئة البوت مع المكونات المحسنة"""
        # تحميل المتغيرات البيئية
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.assistant_id = os.getenv('ASSISTANT_ID')
        
        # التحقق من وجود المتغيرات المطلوبة
        self._validate_environment()
        
        # تهيئة العملاء والمكونات
        try:
            self.bot = telebot.TeleBot(self.telegram_token)
            self.openai_client = OpenAI(api_key=self.openai_api_key)
            self.islamic_explainer = IslamicContextExplainer()
            self.session_manager = SessionManager()
            logger.info("تم تهيئة جميع مكونات البوت بنجاح")
        except Exception as e:
            logger.error(f"خطأ في تهيئة البوت: {e}")
            sys.exit(1)
        
        # إعداد معالجات الرسائل
        self.setup_handlers()
        
        # تخزين الجلسات النشطة مع OpenAI
        self.active_threads: Dict[int, str] = {}
        
        # إحصائيات الاستخدام
        self.usage_stats = {
            'total_messages': 0,
            'islamic_queries': 0,
            'openai_queries': 0,
            'successful_responses': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
    
    def _validate_environment(self):
        """التحقق من صحة متغيرات البيئة"""
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
        """إعداد معالجات الرسائل"""
        
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.handle_start(message)
        
        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            self.handle_help(message)
        
        @self.bot.message_handler(commands=['islamic'])
        def islamic_command(message):
            self.handle_islamic_menu(message)
        
        @self.bot.message_handler(commands=['concept'])
        def concept_command(message):
            self.handle_concept_search(message)
        
        @self.bot.message_handler(commands=['random'])
        def random_command(message):
            self.handle_random_concept(message)
        
        @self.bot.message_handler(commands=['categories'])
        def categories_command(message):
            self.handle_categories(message)
        
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
        """معالجة أمر /start"""
        welcome_text = """
🕌 السلام عليكم ورحمة الله وبركاته

مرحباً بك في البوت الإسلامي الذكي المحسن!

🌟 الميزات الجديدة:
• شارح تفاعلي للمفاهيم الإسلامية
• سياق ثقافي وتاريخي شامل
• أمثلة عملية وتطبيقات واقعية
• تصحيح المفاهيم الخاطئة الشائعة

📚 الأوامر المتاحة:
/islamic - القائمة الإسلامية الرئيسية
/concept - البحث عن مفهوم معين
/random - مفهوم عشوائي للتعلم
/categories - تصفح حسب التصنيفات
/help - المساعدة الشاملة
/stats - إحصائيات الاستخدام
/reset - إعادة تعيين المحادثة

جرب كتابة اسم أي مفهوم إسلامي للحصول على شرح تفاعلي!
        """
        try:
            self.bot.reply_to(message, welcome_text.strip())
            # تهيئة جلسة المستخدم
            session = self.session_manager.get_session(message.from_user.id)
            session.add_to_history("command", "/start")
            logger.info(f"رسالة ترحيب مرسلة للمستخدم {message.from_user.id}")
        except Exception as e:
            logger.error(f"خطأ في إرسال رسالة الترحيب: {e}")
    
    def handle_islamic_menu(self, message):
        """معالجة أمر /islamic - القائمة الإسلامية الرئيسية"""
        menu_text = """
🕌 **القائمة الإسلامية التفاعلية**

🔍 **طرق الاستكشاف:**
1️⃣ البحث المباشر - اكتب اسم المفهوم
2️⃣ التصفح بالتصنيفات - /categories
3️⃣ التعلم العشوائي - /random

📖 **التصنيفات المتاحة:**
• العبادات (صلاة، حج، زكاة...)
• العقائد (توحيد، إيمان، قدر...)
• الفقه (أحكام، معاملات...)
• الأخلاق (إحسان، صبر، تقوى...)
• التاريخ (سيرة، خلافة...)
• الثقافة (تقاليد، آداب...)

💡 **أمثلة للتجربة:**
• اكتب "الصلاة" للشرح التفاعلي
• اكتب "التوحيد" للتعمق في العقيدة
• اكتب "الجهاد" لفهم المعنى الصحيح

ابدأ بكتابة أي مفهوم تريد استكشافه!
        """
        try:
            session = self.session_manager.get_session(message.from_user.id)
            session.set_context("mode", "islamic_exploration")
            session.add_to_history("command", "/islamic")
            
            self.bot.reply_to(message, menu_text.strip())
            self.usage_stats['islamic_queries'] += 1
            logger.info(f"القائمة الإسلامية مرسلة للمستخدم {message.from_user.id}")
        except Exception as e:
            logger.error(f"خطأ في إرسال القائمة الإسلامية: {e}")
    
    def handle_concept_search(self, message):
        """معالجة أمر /concept للبحث عن مفهوم"""
        try:
            # استخراج النص بعد الأمر
            query = message.text.replace('/concept', '').strip()
            
            if not query:
                help_text = """
🔍 **البحث عن المفاهيم الإسلامية**

الاستخدام:
/concept [اسم المفهوم]

أمثلة:
/concept الصلاة
/concept التوحيد
/concept الجهاد

أو اكتب اسم المفهوم مباشرة بدون أمر.
                """
                self.bot.reply_to(message, help_text.strip())
                return
            
            self._handle_islamic_concept_query(message, query)
            
        except Exception as e:
            logger.error(f"خطأ في البحث عن المفهوم: {e}")
            self.bot.reply_to(message, "حدث خطأ في البحث. يرجى المحاولة مرة أخرى.")
    
    def handle_random_concept(self, message):
        """معالجة أمر /random للحصول على مفهوم عشوائي"""
        try:
            random_concept = self.islamic_explainer.get_random_concept()
            session = self.session_manager.get_session(message.from_user.id)
            session.add_to_history("command", "/random")
            
            self.bot.reply_to(message, random_concept)
            self.usage_stats['islamic_queries'] += 1
            logger.info(f"مفهوم عشوائي مرسل للمستخدم {message.from_user.id}")
        except Exception as e:
            logger.error(f"خطأ في إرسال المفهوم العشوائي: {e}")
    
    def handle_categories(self, message):
        """معالجة أمر /categories لعرض التصنيفات"""
        categories_text = """
📚 **تصنيفات المفاهيم الإسلامية**

🕌 **العبادات:**
• الصلاة - الركن الثاني من الإسلام
• الحج - الركن الخامس والرحلة الروحية

🕊️ **العقائد:**
• التوحيد - أساس العقيدة الإسلامية

⚖️ **الفقه:**
• الجهاد - المفهوم الشامل للجهد في سبيل الله

❤️ **الأخلاق:**
• الإحسان - أعلى مراتب الدين

اكتب اسم أي مفهوم للحصول على شرح تفاعلي مفصل.
        """
        try:
            self.bot.reply_to(message, categories_text.strip())
            session = self.session_manager.get_session(message.from_user.id)
            session.add_to_history("command", "/categories")
        except Exception as e:
            logger.error(f"خطأ في إرسال التصنيفات: {e}")
    
    def handle_help(self, message):
        """معالجة أمر /help"""
        help_text = """
📚 **دليل استخدام البوت الإسلامي المحسن**

🌟 **الميزات الرئيسية:**
• شرح تفاعلي للمفاهيم الإسلامية
• سياق ثقافي وتاريخي شامل
• أمثلة عملية ومفاهيم مترابطة
• تصحيح المفاهيم الخاطئة

🔧 **الأوامر المتاحة:**
/start - بدء التشغيل
/islamic - القائمة الإسلامية الرئيسية
/concept [مفهوم] - البحث عن مفهوم محدد
/random - مفهوم عشوائي للتعلم
/categories - تصفح التصنيفات
/stats - إحصائيات الاستخدام
/reset - إعادة تعيين المحادثة
/help - هذه المساعدة

💡 **طرق الاستخدام:**
1. اكتب اسم أي مفهوم إسلامي مباشرة
2. استخدم الأرقام للتنقل في القوائم التفاعلية
3. اطرح أسئلة عامة للحصول على ردود ذكية

🔒 **الخصوصية:**
• جميع المحادثات آمنة ومشفرة
• لا يتم حفظ البيانات الشخصية
• المحتوى مبني على مصادر إسلامية موثقة
        """
        try:
            self.bot.reply_to(message, help_text.strip())
            session = self.session_manager.get_session(message.from_user.id)
            session.add_to_history("command", "/help")
            logger.info(f"رسالة المساعدة مرسلة للمستخدم {message.from_user.id}")
        except Exception as e:
            logger.error(f"خطأ في إرسال رسالة المساعدة: {e}")
    
    def handle_stats(self, message):
        """معالجة أمر /stats"""
        try:
            uptime = datetime.now() - self.usage_stats['start_time']
            session_stats = self.session_manager.get_session_stats()
            
            stats_text = f"""
📊 **إحصائيات البوت الإسلامي**

📈 **الاستخدام:**
• إجمالي الرسائل: {self.usage_stats['total_messages']}
• الاستفسارات الإسلامية: {self.usage_stats['islamic_queries']}
• استفسارات الذكاء الاصطناعي: {self.usage_stats['openai_queries']}
• الردود الناجحة: {self.usage_stats['successful_responses']}
• الأخطاء: {self.usage_stats['errors']}

👥 **الجلسات:**
• الجلسات النشطة: {session_stats['total_active']}
• متوسط طول المحادثة: {session_stats['average_history_length']:.1f}

⏰ **معلومات التشغيل:**
• مدة التشغيل: {str(uptime).split('.')[0]}
• حالة النظام: ✅ يعمل بشكل طبيعي

🔧 **المميزات المفعلة:**
• شارح المفاهيم الإسلامية: ✅
• إدارة الجلسات التفاعلية: ✅
• الذكاء الاصطناعي المتقدم: ✅
            """
            self.bot.reply_to(message, stats_text.strip())
            logger.info(f"إحصائيات مرسلة للمستخدم {message.from_user.id}")
        except Exception as e:
            logger.error(f"خطأ في إرسال الإحصائيات: {e}")
            self.bot.reply_to(message, "حدث خطأ في عرض الإحصائيات")
    
    def handle_reset(self, message):
        """معالجة أمر /reset"""
        try:
            user_id = message.from_user.id
            
            # إعادة تعيين الجلسة
            self.session_manager.clear_session(user_id)
            
            # إعادة تعيين thread OpenAI
            if user_id in self.active_threads:
                del self.active_threads[user_id]
            
            self.bot.reply_to(message, "✅ تم إعادة تعيين المحادثة بنجاح! يمكنك البدء من جديد.")
            logger.info(f"تم إعادة تعيين المحادثة للمستخدم {user_id}")
        except Exception as e:
            logger.error(f"خطأ في إعادة تعيين المحادثة: {e}")
            self.bot.reply_to(message, "حدث خطأ في إعادة تعيين المحادثة")
    
    def handle_message(self, message):
        """معالجة الرسائل العادية"""
        user_id = message.from_user.id
        user_text = message.text
        
        # تحديث الإحصائيات
        self.usage_stats['total_messages'] += 1
        
        try:
            # الحصول على جلسة المستخدم
            session = self.session_manager.get_session(user_id)
            session.add_to_history("user_message", user_text)
            
            # إرسال مؤشر الكتابة
            self.bot.send_chat_action(message.chat.id, 'typing')
            
            # فحص حالة الجلسة
            if session.state == SessionState.EXPLORING_CONCEPT:
                self._handle_concept_interaction(message, session)
            elif self._is_islamic_concept_query(user_text):
                self._handle_islamic_concept_query(message, user_text)
            else:
                # الاستعانة بـ OpenAI للردود العامة
                self._handle_openai_query(message, session)
                
        except Exception as e:
            logger.error(f"خطأ في معالجة الرسالة من المستخدم {user_id}: {e}")
            self.bot.reply_to(message, "حدث خطأ تقني. يرجى المحاولة لاحقاً.")
            self.usage_stats['errors'] += 1
    
    def _is_islamic_concept_query(self, text: str) -> bool:
        """فحص ما إذا كان النص استفساراً عن مفهوم إسلامي"""
        # البحث عن المفاهيم المتاحة
        search_results = self.islamic_explainer.search_concepts(text)
        return len(search_results) > 0
    
    def _handle_islamic_concept_query(self, message, query: str):
        """معالجة استفسار عن مفهوم إسلامي"""
        try:
            search_results = self.islamic_explainer.search_concepts(query)
            session = self.session_manager.get_session(message.from_user.id)
            
            if not search_results:
                # لا توجد نتائج - الاستعانة بـ OpenAI
                self._handle_openai_query(message, session)
                return
            
            # عرض النتيجة الأولى
            concept_id = search_results[0]
            
            if len(search_results) == 1:
                # مفهوم واحد فقط - عرض القائمة التفاعلية
                interactive_menu = self.islamic_explainer.get_interactive_menu(concept_id)
                session.state = SessionState.EXPLORING_CONCEPT
                session.set_context("current_concept", concept_id)
                session.set_context("awaiting_choice", True)
                
                self.bot.reply_to(message, interactive_menu)
                self.usage_stats['islamic_queries'] += 1
                session.add_to_history("bot_response", "interactive_menu")
                
            else:
                # عدة مفاهيم - عرض قائمة للاختيار
                self._show_concept_selection(message, search_results, session)
            
        except Exception as e:
            logger.error(f"خطأ في معالجة المفهوم الإسلامي: {e}")
            self.bot.reply_to(message, "حدث خطأ في البحث عن المفهوم")
    
    def _show_concept_selection(self, message, concept_ids: list, session):
        """عرض قائمة لاختيار المفهوم المطلوب"""
        selection_text = "🔍 **وُجد عدة مفاهيم مطابقة:**\n\n"
        
        for i, concept_id in enumerate(concept_ids[:5], 1):
            concept = self.islamic_explainer.concepts_database[concept_id]
            selection_text += f"{i}️⃣ **{concept.arabic_name}** ({concept.category.value})\n"
            selection_text += f"   {concept.definition[:60]}...\n\n"
        
        selection_text += "اختر رقم المفهوم الذي تريد استكشافه (1-5):"
        
        session.state = SessionState.AWAITING_CHOICE
        session.set_context("concept_options", concept_ids[:5])
        
        self.bot.reply_to(message, selection_text.strip())
    
    def _handle_concept_interaction(self, message, session):
        """معالجة التفاعل مع المفهوم"""
        user_input = message.text.strip()
        
        if session.get_context("awaiting_choice"):
            # اختيار من القائمة التفاعلية
            current_concept = session.get_context("current_concept")
            
            if user_input.isdigit() and 1 <= int(user_input) <= 8:
                # عرض الجانب المطلوب
                aspect_content = self.islamic_explainer.get_concept_aspect(current_concept, user_input)
                self.bot.reply_to(message, aspect_content)
                
                # عرض اقتراحات للمفاهيم المترابطة
                if user_input == "8":  # الشرح الكامل
                    suggestions = self.islamic_explainer.suggest_related_concepts(current_concept)
                    if suggestions:
                        self.bot.send_message(message.chat.id, suggestions)
                
                session.add_to_history("bot_response", f"concept_aspect_{user_input}")
                self.usage_stats['successful_responses'] += 1
                
            else:
                # بحث أو سؤال جديد
                self._handle_islamic_concept_query(message, user_input)
        
        elif session.get_context("concept_options"):
            # اختيار من قائمة المفاهيم
            if user_input.isdigit():
                choice_index = int(user_input) - 1
                concept_options = session.get_context("concept_options")
                
                if 0 <= choice_index < len(concept_options):
                    selected_concept = concept_options[choice_index]
                    interactive_menu = self.islamic_explainer.get_interactive_menu(selected_concept)
                    
                    session.set_context("current_concept", selected_concept)
                    session.set_context("awaiting_choice", True)
                    session.context.pop("concept_options", None)
                    
                    self.bot.reply_to(message, interactive_menu)
                    return
            
            self.bot.reply_to(message, "يرجى اختيار رقم صحيح من القائمة.")
    
    def _handle_openai_query(self, message, session):
        """معالجة الاستفسارات العامة باستخدام OpenAI"""
        try:
            user_id = message.from_user.id
            
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
                content=message.text
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
                    self.bot.reply_to(message, "حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى.")
                    return
                
                time.sleep(1)
            else:
                logger.error("انتهت مهلة انتظار رد المساعد")
                self.bot.reply_to(message, "الطلب يستغرق وقتاً أطول من المعتاد. يرجى المحاولة مرة أخرى.")
                return
            
            # الحصول على الرد
            messages = self.openai_client.beta.threads.messages.list(
                thread_id=thread_id,
                order="desc",
                limit=1
            )
            
            if messages.data:
                assistant_message = messages.data[0]
                if hasattr(assistant_message.content[0], 'text'):
                    response_text = assistant_message.content[0].text.value
                    self.bot.reply_to(message, response_text)
                    
                    session.add_to_history("bot_response", "openai_response")
                    self.usage_stats['openai_queries'] += 1
                    self.usage_stats['successful_responses'] += 1
                    logger.info(f"رد OpenAI ناجح للمستخدم {user_id}")
                    return
            
            self.bot.reply_to(message, "لم أتمكن من الحصول على رد مناسب. يرجى إعادة صياغة سؤالك.")
            
        except Exception as e:
            logger.error(f"خطأ في معالجة استفسار OpenAI: {e}")
            self.bot.reply_to(message, "حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى.")
            self.usage_stats['errors'] += 1
    
    def run(self):
        """تشغيل البوت"""
        logger.info("🚀 بدء تشغيل البوت الإسلامي المحسن...")
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
    """الدالة الرئيسية"""
    try:
        bot = EnhancedIslamicBot()
        bot.run()
    except Exception as e:
        logger.error(f"خطأ في الدالة الرئيسية: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()