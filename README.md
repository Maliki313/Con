# بوت تيليجرام ذكي مع OpenAI

بوت تيليجرام متطور يستخدم مساعد OpenAI للرد على الرسائل باللغة العربية والإنجليزية.

## المميزات

- 🤖 تكامل مع OpenAI Assistant API
- 📱 دعم كامل لتيليجرام
- 🔄 معالجة الأخطاء المتقدمة
- 📝 تسجيل شامل للأحداث
- ⚡ ردود سريعة وذكية
- 🌐 دعم متعدد اللغات

## المتطلبات

- Python 3.8+
- حساب Telegram Bot
- مفتاح OpenAI API
- معرف OpenAI Assistant

## التثبيت

1. استنساخ المستودع:
```bash
git clone https://github.com/Maliki313/Con.git
cd Con
```

2. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

3. إعداد المتغيرات البيئية:
```bash
export TELEGRAM_TOKEN="your_telegram_bot_token"
export OPENAI_API_KEY="your_openai_api_key"
export ASSISTANT_ID="your_assistant_id"
```

## الاستخدام

تشغيل البوت:
```bash
python main.py
```

## الأوامر المتاحة

- `/start` - بدء المحادثة
- `/help` - عرض المساعدة
- إرسال أي رسالة للحصول على رد ذكي

## إعداد Telegram Bot

1. تحدث مع [@BotFather](https://t.me/botfather)
2. أنشئ بوت جديد بالأمر `/newbot`
3. احفظ التوكن المرسل

## إعداد OpenAI Assistant

1. انتقل إلى [OpenAI Platform](https://platform.openai.com/)
2. أنشئ مساعد جديد
3. احفظ معرف المساعد

## البنية

```
Con/
├── main.py              # الملف الرئيسي للبوت
├── requirements.txt     # متطلبات Python
├── Procfile            # إعداد Heroku
├── README.md           # هذا الملف
└── .github/            # إعدادات GitHub
```

## النشر

### Heroku

```bash
heroku create your-bot-name
heroku config:set TELEGRAM_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
heroku config:set ASSISTANT_ID=your_id
git push heroku main
```

### Railway

```bash
railway login
railway init
railway add
railway deploy
```

## المساهمة

1. Fork المستودع
2. أنشئ فرع للميزة الجديدة
3. Commit التغييرات
4. Push للفرع
5. افتح Pull Request

## الترخيص

MIT License - راجع ملف LICENSE للتفاصيل

## الدعم

للدعم والاستفسارات، افتح Issue في المستودع.