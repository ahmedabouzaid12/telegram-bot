import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from utils import get_access_token, thread1, thread2, execute_attempt

# إعدادات البوت
TOKEN = "7690211912:AAGKR2tb3ygmsG7vhB4bf0sn5zFmc355KEg"
ADMIN_USERNAME = "awwwan105"  # حط اسمك في تيليجرام هنا (بدون @)

# تحميل البيانات من ملف JSON
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {"allowed_users": [], "user_success_count": {}, "user_data": {}}

# حفظ البيانات في ملف JSON
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    welcome_message = """
    مرحبًا بك في بوت كسر الرقم! 🚀
    اضغط على الزر عشان تبدأ العملية.
    """
    keyboard = [[InlineKeyboardButton("كسر الرقم", callback_data="break_number")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(welcome_message, reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user.username
    user_id = query.from_user.id
    
    if query.data == "break_number":
        if user not in data["allowed_users"] and user != ADMIN_USERNAME:
            query.answer("⛔ مش مسموحلك تستخدم البوت، تواصل مع الأدمن!")
            return
        
        query.answer()
        query.edit_message_text("📳 الرجاء إدخال رقم فودافون صاحب العائلة:")
        data["user_data"][user_id] = {"step": "number"}
        save_data(data)

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = update.message.from_user.username
    text = update.message.text

    if user_id not in data["user_data"]:
        update.message.reply_text("اضغط على /start لبدء العملية!")
        return

    current_step = data["user_data"][user_id]["step"]

    if current_step == "number":
        data["user_data"][user_id]["number"] = text
        data["user_data"][user_id]["step"] = "password_owner"
        update.message.reply_text("🔐 الرجاء إدخال باسورد صاحب العائلة:")
    elif current_step == "password_owner":
        data["user_data"][user_id]["password_owner"] = text
        data["user_data"][user_id]["step"] = "member1"
        update.message.reply_text("📳 الرجاء إدخال رقم الفرد الأول:")
    elif current_step == "member1":
        data["user_data"][user_id]["member1"] = text
        data["user_data"][user_id]["step"] = "password1"
        update.message.reply_text("🔐 الرجاء إدخال باسورد الفرد الأول:")
    elif current_step == "password1":
        data["user_data"][user_id]["password1"] = text
        data["user_data"][user_id]["step"] = "member2"
        update.message.reply_text("📳 الرجاء إدخال رقم الفرد الثاني:")
    elif current_step == "member2":
        data["user_data"][user_id]["member2"] = text
        data["user_data"][user_id]["step"] = "password2"
        update.message.reply_text("🔐 الرجاء إدخال باسورد الفرد الثاني:")
    elif current_step == "password2":
        data["user_data"][user_id]["password2"] = text
        data["user_data"][user_id]["step"] = "attempts"
        update.message.reply_text("🔄 الرجاء إدخال عدد المحاولات:")
    elif current_step == "attempts":
        try:
            attempts = int(text)
            data["user_data"][user_id]["attempts"] = attempts
            data["user_data"][user_id]["step"] = "running"
            update.message.reply_text("⏳ جاري بدء العملية...")
            
            for attempt in range(1, attempts + 1):
                success = False
                while not success:
                    success = execute_attempt(user_id, attempt, attempts, context, data["user_data"][user_id])
                    if not success:
                        import time
                        time.sleep(5)
            
            update.message.reply_text("🏁 تم الانتهاء من جميع المحاولات بنجاح!")
            data["user_success_count"][user] = data["user_success_count"].get(user, 0) + 1
            del data["user_data"][user_id]
        except ValueError:
            update.message.reply_text("⚠️ الرجاء إدخال رقم صحيح لعدد المحاولات!")
    
    save_data(data)

def admin_add(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    if user != ADMIN_USERNAME:
        update.message.reply_text("⛔ الأدمن بس هو اللي يقدر يضيف مستخدمين!")
        return
    try:
        new_user = context.args[0]
        if new_user not in data["allowed_users"]:
            data["allowed_users"].append(new_user)
            save_data(data)
            update.message.reply_text(f"✅ تم إضافة {new_user} بنجاح!")
        else:
            update.message.reply_text("⚠️ المستخدم موجود بالفعل!")
    except IndexError:
        update.message.reply_text("📝 اكتب اسم المستخدم بعد الأمر، مثال: /add username")

def admin_remove(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    if user != ADMIN_USERNAME:
        update.message.reply_text("⛔ الأدمن بس هو اللي يقدر يحذف مستخدمين!")
        return
    try:
        user_to_remove = context.args[0]
        if user_to_remove in data["allowed_users"]:
            data["allowed_users"].remove(user_to_remove)
            save_data(data)
            update.message.reply_text(f"✅ تم حذف {user_to_remove} بنجاح!")
        else:
            update.message.reply_text("⚠️ المستخدم مش موجود!")
    except IndexError:
        update.message.reply_text("📝 اكتب اسم المستخدم بعد الأمر، مثال: /remove username")

def admin_stats(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    if user != ADMIN_USERNAME:
        update.message.reply_text("⛔ الأدمن بس هو اللي يقدر يشوف الإحصائيات!")
        return
    stats = "\n".join([f"@{user}: {count} مرة" for user, count in data["user_success_count"].items()])
    update.message.reply_text(f"📊 إحصائيات النجاح:\n{stats if stats else 'لا توجد إحصائيات بعد!'}")

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CommandHandler("add", admin_add))
    dp.add_handler(CommandHandler("remove", admin_remove))
    dp.add_handler(CommandHandler("stats", admin_stats))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()