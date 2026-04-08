import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os
import time

# --- 1. إعداد سيرفر الويب (Flask) لمنع توقف الاستضافة ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running Live!"

def run():
    # Render يمرر المنفذ تلقائياً عبر متغير بيئة PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. إعداد البوت (ضع التوكن الخاص بك هنا) ---
TOKEN = '8738316553:AAFvxe-8QmQygsO72c8k2UR37oRka811Xss'
bot = telebot.TeleBot(TOKEN)

# بيانات الأسئلة (BEM 2026)
DATA = {
    "ar": {"n": "📖 العربية", "q": "📝 أعرب: 'يا طالعاً جبلاً'.", "a": "✅ طالعاً: منادى شبيه بالمضاف، جبلاً: مفعول به لاسم الفاعل."},
    "ma": {"n": "📐 الرياضيات", "q": "📝 ما شرط الارتباط الخطي لشعاعين؟", "a": "✅ الشرط هو: xy' - yx' = 0."},
    "sc": {"n": "🔬 العلوم", "q": "📝 أين يتم هضم النشاء؟", "a": "✅ يبدأ في الفم (الأميلاز اللعابي) ويكتمل في المعي الدقيق."},
    "h": {"n": "📜 الاجتماعيات", "q": "📝 متى اندلعت الثورة التحريرية؟", "a": "✅ في 1 نوفمبر 1954."}
}

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🔥 اختبارات BEM", callback_data="sec_ex"),
        types.InlineKeyboardButton("📚 المصادر", url="https://www.dzexams.com/ar/4am")
    )
    bot.send_message(m.chat.id, "🦅 **مرحباً بك في بوت مراجعة BEM 2026**\nاختر مادة للبدء:", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    cid, mid = call.message.chat.id, call.message.message_id
    if call.data == "sec_ex":
        kb = types.InlineKeyboardMarkup(row_width=2)
        for k in DATA: kb.add(types.InlineKeyboardButton(DATA[k]["n"], callback_data=f"ex_{k}"))
        bot.edit_message_text("📖 اختر المادة:", cid, mid, reply_markup=kb)
    elif call.data.startswith("ex_"):
        c = call.data.split("_")[1]
        kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("👁️ كشف الحل", callback_data=f"sol_{c}"))
        bot.edit_message_text(DATA[c]["q"], cid, mid, reply_markup=kb)
    elif call.data.startswith("sol_"):
        c = call.data.split("_")[1]
        bot.edit_message_text(DATA[c]["a"], cid, mid)

# --- 3. تشغيل البوت مع الحماية من التوقف ---
if __name__ == '__main__':
    keep_alive() # تشغيل Flask في الخلفية
    print("البوت انطلق...")
    
    # حلقة تكرار لمنع توقف البوت عند حدوث أخطاء في الشبكة
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"حدث خطأ: {e}")
            time.sleep(5) # انتظر 5 ثواني ثم حاول مجدداً
