import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from api import get_access_token, thread1, thread2
from utils import save_data, load_data
from threading import Thread
import time
import telegram.error

# إعدادات البوت
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 1105434173
FIXED_QUOTA = 40

# بيانات المستخدمين
user_data = {}
allowed_users = load_data("allowed_users.json", default=[])
stats = load_data("stats.json", default={})

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "No Username"
    
    keyboard = [[InlineKeyboardButton("كسر الرقم", callback_data="break")]]
    if user_id == ADMIN_ID:
        keyboard.extend([
            [InlineKeyboardButton("السماح لمستخدم", callback_data="allow_list")],
            [InlineKeyboardButton("حذف مستخدم", callback_data="delete_list")],
            [InlineKeyboardButton("الإحصائيات", callback_data="stats")]
        ])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحبًا! 🚀 اضغط 'كسر الرقم' لبدء العملية.", reply_markup=reply_markup)
    
    if user_id != ADMIN_ID and user_id not in allowed_users:
        try:
            context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"طلب سماح من:\nID: {user_id}\nUsername: @{username}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("سماح", callback_data=f"allow_{user_id}"), InlineKeyboardButton("رفض", callback_data=f"deny_{user_id}")]
                ])
            )
        except telegram.error.BadRequest as e:
            print(f"فشل إرسال طلب السماح إلى الأدمن: {e}")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    text = update.message.text
    
    if user_id not in user_data or "step" not in user_data[user_id]:
        return
    
    step = user_data[user_id]["step"]
    if step == "number":
        user_data[user_id]["number"] = text
        user_data[user_id]["step"] = "password_owner"
        update.message.reply_text("🔐 باسورد صاحب العائلة:")
    elif step == "password_owner":
        user_data[user_id]["password_owner"] = text
        user_data[user_id]["step"] = "member1"
        update.message.reply_text("📳 رقم الفرد الأول:")
    elif step == "member1":
        user_data[user_id]["member1"] = text
        user_data[user_id]["step"] = "password1"
        update.message.reply_text("🔐 باسورد الفرد الأول:")
    elif step == "password1":
        user_data[user_id]["password1"] = text
        user_data[user_id]["step"] = "member2"
        update.message.reply_text("📳 رقم الفرد الثاني:")
    elif step == "member2":
        user_data[user_id]["member2"] = text
        user_data[user_id]["step"] = "password2"
        update.message.reply_text("🔐 باسورد الفرد الثاني:")
    elif step == "password2":
        user_data[user_id]["password2"] = text
        user_data[user_id]["step"] = "attempts"
        update.message.reply_text("🔄 عدد المحاولات:")
    elif step == "attempts":
        try:
            attempts = int(text)
            user_data[user_id]["attempts"] = attempts
            user_data[user_id]["quota"] = FIXED_QUOTA
            user_data[user_id]["step"] = "running"
            update.message.reply_text("⏳ جاري التنفيذ...")
            Thread(target=execute_attempts, args=(context, user_id)).start()
        except ValueError:
            update.message.reply_text("⚠️ أدخل رقم صحيح!")

def execute_attempts(context: CallbackContext, user_id: int) -> None:
    data = user_data[user_id]
    access_token = get_access_token(data["number"], data["password_owner"])
    
    if not access_token:
        context.bot.send_message(chat_id=user_id, text="⚠️ مشكلة في تسجيل الدخول! جرب تاني.")
        try:
            context.bot.send_message(chat_id=ADMIN_ID, text=f"خطأ في التوكن لـ {user_id}")
        except telegram.error.BadRequest as e:
            print(f"فشل إرسال إشعار الخطأ إلى الأدمن: {e}")
        return
    
    successful_attempts = 0
    for attempt in range(data["attempts"]):  # لكل محاولة من attempts
        for i in range(30):  # 30 محاولة كحد أقصى لكل تكرار
            try:
                time.sleep(9)
                thread1(10, data["member1"], access_token, data["number"])
                time.sleep(9)
                thread2(10, data["member2"], access_token, data["number"])
                time.sleep(8)
                t1 = Thread(target=thread1, args=(data["quota"], data["member1"], access_token, data["number"]))
                t2 = Thread(target=thread2, args=(data["quota"], data["member2"], access_token, data["number"]))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
                time.sleep(3)
                with open("a1.text", "r") as f1, open("a2.text", "r") as f2:
                    if f1.read() + f2.read() == "{}40{}40":
                        successful_attempts += 1
                        context.bot.send_message(chat_id=user_id, text=f"✅ نجاح المحاولة {successful_attempts}/{data['attempts']}")
                        os.remove("a1.text")
                        os.remove("a2.text")
                        break  # نخرج من الـ 30 لو نجحت
            except FileNotFoundError:
                continue  # لو فشل، نكمل المحاولة التالية ضمن الـ 30
    
    context.bot.send_message(chat_id=user_id, text="🏁 تم الانتهاء من جميع المحاولات!")
    stats[str(user_id)] = stats.get(str(user_id), 0) + 1
    save_data("stats.json", stats)
    del user_data[user_id]

def button(update: Update, context: CallbackContext) -> None:
    global allowed_users, stats
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    
    query.answer()
    
    if data == "break":
        if user_id != ADMIN_ID and user_id not in allowed_users:
            query.edit_message_text("⛔ غير مسموح لك! انتظر موافقة الأدمن.")
            return
        user_data[user_id] = {"step": "number"}
        query.edit_message_text("📞 رقم صاحب العائلة:")
    
    elif data == "allow_list" and user_id == ADMIN_ID:
        query.edit_message_text("جاري انتظار طلبات السماح...")
    
    elif data.startswith("allow_") and user_id == ADMIN_ID:
        try:
            target_id = int(data.split("_")[1])
            if target_id not in allowed_users:
                allowed_users.append(target_id)
                save_data("allowed_users.json", allowed_users)
                if str(target_id) not in stats:
                    stats[str(target_id)] = 0
                    save_data("stats.json", stats)
                context.bot.send_message(chat_id=target_id, text="✅ تم السماح لك! اضغط /start مرة أخرى.")
            query.edit_message_text("تم السماح!")
        except (ValueError, telegram.error.BadRequest) as e:
            query.edit_message_text(f"خطأ: {e}")
    
    elif data.startswith("deny_") and user_id == ADMIN_ID:
        query.edit_message_text("تم الرفض!")
    
    elif data == "delete_list" and user_id == ADMIN_ID:
        allowed_users = load_data("allowed_users.json", default=[])
        if not allowed_users:
            query.edit_message_text("لا يوجد مستخدمين مسموح لهم!")
            return
        keyboard = [[InlineKeyboardButton(f"ID: {uid}", callback_data=f"delete_{uid}")] for uid in allowed_users]
        query.edit_message_text("اختر مستخدم لحذفه:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith("delete_") and user_id == ADMIN_ID:
        try:
            target_id = int(data.split("_")[1])
            allowed_users = load_data("allowed_users.json", default=[])
            if target_id in allowed_users:
                allowed_users.remove(target_id)
                save_data("allowed_users.json", allowed_users)
                query.edit_message_text("تم الحذف!")
            else:
                query.edit_message_text("المستخدم غير موجود!")
        except ValueError as e:
            query.edit_message_text(f"خطأ: {e}")
    
    elif data == "stats" and user_id == ADMIN_ID:
        stats_text = "\n".join([f"ID: {uid} - المرات: {count}" for uid, count in stats.items()])
        query.edit_message_text(f"الإحصائيات:\n{stats_text or 'لا توجد بيانات'}")

def error_handler(update: Update, context: CallbackContext) -> None:
    print(f"حدث خطأ: {context.error}")

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()