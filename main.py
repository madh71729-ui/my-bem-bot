import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os
import time

# --- 1. إعداد خادم الويب (Flask) ---
app = Flask('')

@app.route('/')
def home():
    return "بوت مراجعة BEM 2026 يعمل بكامل طاقته!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. إعداد البوت ---
TOKEN = '8738316553:AAFvxe-8QmQygsO72c8k2UR37oRka811Xss'
bot = telebot.TeleBot(TOKEN)

# --- بنك الأسئلة الكامل لجميع المواد ---
DATA = {
    "ar": {"n": "📖 العربية", "q": "📝 أعرب: 'يا طالعاً جبلاً'.", "a": "✅ طالعاً: منادى شبيه بالمضاف منصوب."},
    "ma": {"n": "📐 الرياضيات", "q": "📝 ما هو قانون القاسم المشترك الأكبر PGCD؟", "a": "✅ هو أكبر عدد يقسم عددين طبيعيين في آن واحد، ونستخدم خوارزمية إقليدس لحسابه."},
    "sc": {"n": "🔬 العلوم", "q": "📝 ما هو دور المعي الدقيق؟", "a": "✅ امتصاص المغذيات عن طريق الزغابات المعوية."},
    "ph": {"n": "⚡ الفيزياء", "q": "📝 ما هي وحدة قياس القوة؟", "a": "✅ النيوتن (N)."},
    "hi": {"n": "📜 التاريخ", "q": "📝 متى كانت معركة نوارين؟", "a": "✅ 20 أكتوبر 1827."},
    "ge": {"n": "🌍 الجغرافيا", "q": "📝 ما هي مساحة الجزائر؟", "a": "✅ 2,381,741 كم²."},
    "fr": {"n": "🇫🇷 الفرنسية", "q": "📝 Qu'est-ce qu'un texte argumentatif ?", "a": "✅ C'est un texte qui vise à convaincre le lecteur."},
    "en": {"n": "🇬🇧 الإنجليزية", "q": "📝 Give the past simple of 'Go'.", "a": "✅ The past simple is: Went."},
    "is": {"n": "🕌 الإسلامية", "q": "📝 ما هو تعريف الحج؟", "a": "✅ هو قصد بيت الله الحرام لأداء مناسك محددة في وقت معلوم."},
    "ci": {"n": "⚖️ المدنية", "q": "📝 ما هي أعلى سلطة في البلاد؟", "a": "✅ المحكمة العليا."}
}

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🚀 ابدأ المراجعة الشاملة", callback_data="sec_ex"),
        types.InlineKeyboardButton("📢 قناة التحديثات", url="https://t.me/your_channel")
    )
    bot.send_message(m.chat.id, "🦅 **مرحباً بك في نسخة BEM 2026 الكاملة**\nتمت إضافة جميع المواد الآن. اختر المادة التي تريد اختبار نفسك فيها:", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    cid, mid = call.message.chat.id, call.message.message_id
    if call.data == "sec_ex":
        kb = types.InlineKeyboardMarkup(row_width=2)
        # توليد الأزرار لجميع المواد تلقائياً
        buttons = [types.InlineKeyboardButton(v["n"], callback_data=f"ex_{k}") for k, v in DATA.items()]
        kb.add(*buttons)
        bot.edit_message_text("📚 قائمة المواد المتوفرة:", cid, mid, reply_markup=kb)
    
    elif call.data.startswith("ex_"):
        c = call.data.split("_")[1]
        kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("👁️ إظهار الإجابة النموذجية", callback_data=f"sol_{c}"),
            types.InlineKeyboardButton("🔙 العودة للمواد", callback_data="sec_ex")
        )
        bot.edit_message_text(f"❓ **سؤال في {DATA[c]['n']}:**\n\n{DATA[c]['q']}", cid, mid, reply_markup=kb)
    
    elif call.data.startswith("sol_"):
        c = call.data.split("_")[1]
        kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 سؤال آخر من هذه المادة", callback_data=f"ex_{c}"), types.InlineKeyboardButton("🔙 قائمة المواد", callback_data="sec_ex"))
        bot.edit_message_text(f"🎯 **الإجابة:**\n\n{DATA[c]['a']}", cid, mid, reply_markup=kb)

# --- 3. تشغيل البوت ---
if __name__ == '__main__':
    keep_alive()
    print("البوت يعمل بجميع المواد...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(5)

