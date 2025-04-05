import requests
import time
import os
import json
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime, date

# إعدادات البوت
TOKEN = "7690211912:AAGKR2tb3ygmsG7vhB4bf0sn5zFmc355KEg"
session = requests.Session()

# قيمة الحصة الثابتة
FIXED_QUOTA = 40

# حالة المستخدم
user_data = {}

# الأدمن (غير الـ ID ده بتاعك)
ADMIN_ID = 1105434173  # حط الـ User ID بتاعك هنا

# مسار ملف JSON لتخزين البيانات
DATA_FILE = "bot_data.json"

# تحميل البيانات من ملف JSON أو إنشاء جديد
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return set(data.get('allowed_users', [])), data.get('usage_stats', {})
    return set(), {}

# حفظ البيانات في ملف JSON
def save_data(allowed_users, usage_stats):
    with open(DATA_FILE, 'w') as f:
        json.dump({
            'allowed_users': list(allowed_users),
            'usage_stats': usage_stats
        }, f)

# تحميل البيانات عند بدء التشغيل
allowed_users, usage_stats = load_data()

def start(update: Update, context: CallbackContext) -> None:
    """إرسال رسالة ترحيبية مع زر البدء وزر الإحصائيات"""
    welcome_message = """
    مرحبًا بك في بوت كسر الرقم! 🚀
    
    هذا البوت مصمم لمساعدتك في إدارة حصص البيانات على فودافون.
    
    اضغط على الزر أدناه لبدء العملية أو لعرض الإحصائيات.
    """
    
    keyboard = [
        [InlineKeyboardButton("كسر الرقم 🔓", callback_data='start_process')],
        [InlineKeyboardButton("عرض الإحصائيات 📊", callback_data='show_stats')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_message, reply_markup=reply_markup)

def allow_user(update: Update, context: CallbackContext) -> None:
    """أمر للأدمن عشان يسمح ليوزر"""
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ هذا الأمر متاح للأدمن فقط.")
        return
    
    try:
        target_user_id = int(context.args[0])
        allowed_users.add(target_user_id)
        save_data(allowed_users, usage_stats)
        update.message.reply_text(f"✅ تم السماح لليوزر {target_user_id} باستخدام البوت.")
    except (IndexError, ValueError):
        update.message.reply_text("⚠️ استخدم الأمر بالشكل الصحيح: /allow <user_id>")

def disallow_user(update: Update, context: CallbackContext) -> None:
    """أمر للأدمن عشان يمنع يوزر"""
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ هذا الأمر متاح للأدمن فقط.")
        return
    
    try:
        target_user_id = int(context.args[0])
        allowed_users.discard(target_user_id)
        save_data(allowed_users, usage_stats)
        update.message.reply_text(f"✅ تم منع اليوزر {target_user_id} من استخدام البوت.")
    except (IndexError, ValueError):
        update.message.reply_text("⚠️ استخدم الأمر بالشكل الصحيح: /disallow <user_id>")

def stats(update: Update, context: CallbackContext) -> None:
    """أمر للأدمن عشان يشوف عدد المرات ليوزر"""
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ هذا الأمر متاح للأدمن فقط.")
        return
    
    try:
        target_user_id = int(context.args[0])
        today = str(date.today())
        if target_user_id in usage_stats and usage_stats[target_user_id]['date'] == today:
            count = usage_stats[target_user_id]['count']
            update.message.reply_text(f"📊 اليوزر {target_user_id} كسر {count} رقم اليوم.")
        else:
            update.message.reply_text(f"📊 اليوزر {target_user_id} لم يكسر أي أرقام اليوم.")
    except (IndexError, ValueError):
        update.message.reply_text("⚠️ استخدم الأمر بالشكل الصحيح: /stats <user_id>")

def show_stats(update: Update, context: CallbackContext) -> None:
    """عرض رسالة للأدمن لإدخال ID المستخدم لعرض الإحصائيات"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id != ADMIN_ID:
        query.edit_message_text("❌ هذا الأمر متاح للأدمن فقط.")
        return
    
    query.answer()
    query.edit_message_text("📊 الرجاء إدخال ID المستخدم لعرض إحصائياته (مثال: 123456789):")
    user_data[user_id] = {'step': 'stats_input'}  # إضافة حالة مؤقتة لاستقبال الـ ID

def start_process(update: Update, context: CallbackContext) -> None:
    """بدء عملية إدخال البيانات مع التحقق من الصلاحية"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id not in allowed_users and user_id != ADMIN_ID:
        query.edit_message_text("❌ غير مصرح لك باستخدام هذا البوت. تواصل مع الأدمن.")
        return
    
    query.answer()
    user_data[user_id] = {
        'step': 'number',
        'attempts': 30,
        'quota': FIXED_QUOTA
    }
    query.edit_message_text(text="🔢 الرجاء إدخال رقم فودافون صاحب العائلة:")

def handle_message(update: Update, context: CallbackContext) -> None:
    """معالجة الرسائل الواردة من المستخدم"""
    user_id = update.message.from_user.id
    text = update.message.text
    
    if user_id not in user_data:
        update.message.reply_text("الرجاء الضغط على /start لبدء العملية.")
        return
    
    current_step = user_data[user_id]['step']
    
    if current_step == 'stats_input':  # معالجة إدخال الـ ID للإحصائيات
        try:
            target_user_id = int(text)
            today = str(date.today())
            if target_user_id in usage_stats and usage_stats[target_user_id]['date'] == today:
                count = usage_stats[target_user_id]['count']
                update.message.reply_text(f"📊 اليوزر {target_user_id} كسر {count} رقم اليوم.")
            else:
                update.message.reply_text(f"📊 اليوزر {target_user_id} لم يكسر أي أرقام اليوم.")
            del user_data[user_id]  # حذف الحالة بعد الانتهاء
        except ValueError:
            update.message.reply_text("⚠️ الرجاء إدخال ID صحيح (رقم فقط). حاول مرة أخرى:")
        return
    
    if current_step == 'number':
        user_data[user_id]['number'] = text
        user_data[user_id]['step'] = 'password_owner'
        update.message.reply_text("🔐 الرجاء إدخال باسورد صاحب العائلة:")
    
    elif current_step == 'password_owner':
        user_data[user_id]['password_owner'] = text
        user_data[user_id]['step'] = 'member1'
        update.message.reply_text("📳 الرجاء إدخال رقم الفرد الأول:")
    
    elif current_step == 'member1':
        user_data[user_id]['member1'] = text
        user_data[user_id]['step'] = 'password1'
        update.message.reply_text("🔐 الرجاء إدخال باسورد الفرد الأول:")
    
    elif current_step == 'password1':
        user_data[user_id]['password1'] = text
        user_data[user_id]['step'] = 'member2'
        update.message.reply_text("📳 الرجاء إدخال رقم الفرد الثاني:")
    
    elif current_step == 'member2':
        user_data[user_id]['member2'] = text
        user_data[user_id]['step'] = 'password2'
        update.message.reply_text("🔐 الرجاء إدخال باسورد الفرد الثاني:")
    
    elif current_step == 'password2':
        user_data[user_id]['password2'] = text
        user_data[user_id]['step'] = 'attempts'
        update.message.reply_text(f"🔄 الرجاء إدخال عدد المحاولات (القيمة الافتراضية {user_data[user_id]['attempts']}):")
    
    elif current_step == 'attempts':
        try:
            attempts = int(text) if text else user_data[user_id]['attempts']
            user_data[user_id]['attempts'] = attempts
            user_data[user_id]['step'] = 'confirm'
            summary = f"""
            ⚙️ إعدادات العملية:
            رقم صاحب العائلة: {user_data[user_id]['number']}
            باسورد صاحب العائلة: {'*' * len(user_data[user_id]['password_owner'])}
            الفرد الأول: {user_data[user_id]['member1']}
            باسورد الفرد الأول: {'*' * len(user_data[user_id]['password1'])}
            الفرد الثاني: {user_data[user_id]['member2']}
            باسورد الفرد الثاني: {'*' * len(user_data[user_id]['password2'])}
            قيمة الحصة: {FIXED_QUOTA} (ثابتة)
            عدد المحاولات: {user_data[user_id]['attempts']}
            """
            keyboard = [
                [InlineKeyboardButton("بدء العملية ✅", callback_data='run_process')],
                [InlineKeyboardButton("إلغاء ❌", callback_data='cancel_process')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(summary, reply_markup=reply_markup)
        except ValueError:
            update.message.reply_text("⚠️ الرجاء إدخال رقم صحيح. حاول مرة أخرى:")

def get_access_token(number, password):
    """الحصول على token الوصول"""
    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    headers = {
        "x-dynatrace": "MT_3_8_2164993384_64-0_a556db1b-4506-43f3-854a-1d2527767923_0_1080_235",
        "x-agent-operatingsystem": "1601266300",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Sherif_Omar",
        "x-agent-version": "2021.12.2",
        "x-agent-build": "493",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.1"
    }
    data = {
        "username": number,
        "password": password,
        "grant_type": "password",
        "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
        "client_id": "my-vodafone-app"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

def execute_attempt(user_id, attempt_num, total_attempts, context):
    """تنفيذ محاولة واحدة مع تحديث الحالة"""
    data = user_data[user_id]
    access_token = get_access_token(data['number'], data['password_owner'])
    
    if not access_token:
        context.bot.send_message(chat_id=user_id, text="❌ فشل في الحصول على token الوصول. تخطي هذه المحاولة.")
        return False
    
    context.bot.send_message(chat_id=user_id, text=f"🔹 بدء المحاولة {attempt_num}/{total_attempts}")
    
    result1 = thread1(data['quota'], data['member1'], access_token, user_id, context)
    time.sleep(5)
    
    result2 = thread2(data['quota'], data['member2'], access_token, user_id, context)
    time.sleep(5)
    
    status_message = f"""
    📊 حالة المحاولة {attempt_num}/{total_attempts}:
    الفرد الأول: {'✅ نجاح' if result1 else '❌ فشل'}
    الفرد الثاني: {'✅ نجاح' if result2 else '❌ فشل'}
    """
    context.bot.send_message(chat_id=user_id, text=status_message)
    
    return result1 and result2

def thread1(quota, member1, access_token, user_id, context):
    """تنفيذ العملية للفرد الأول"""
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "api-host": "ProductOrderingManagement",
        "useCase": "MIProfile",
        "Authorization": f"Bearer {access_token}",
        "api-version": "v2",
        "x-agent-operatingsystem": "9",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Xiaomi Redmi 6A",
        "x-agent-version": "2024.3.2",
        "x-agent-build": "592",
        "msisdn": user_data[user_id]['number'],
        "Accept": "application/json",
        "Accept-Language": "ar",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/4.11.0"
    }
    data = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "createdBy": {"value": "MobileApp"},
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [{"characteristicName": "quotaDist1", "type": "percentage", "value": quota}]
            },
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": user_data[user_id]['number']}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": member1}], "type": "Member"}
            ]
        },
        "type": "QuotaRedistribution"
    }
    
    try:
        response = session.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return True
        else:
            context.bot.send_message(chat_id=user_id, text=f"⚠️ خطأ في الفرد الأول: {response.text}")
            return False
    except Exception as e:
        context.bot.send_message(chat_id=user_id, text=f"❌ خطأ اتصال بالفرد الأول: {str(e)}")
        return False

def thread2(quota, member2, access_token, user_id, context):
    """تنفيذ العملية للفرد الثاني"""
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "Host": "web.vodafone.com.eg",
        "msisdn": user_data[user_id]['number'],
        "Accept-Language": "AR",
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "clientId": "WebsiteConsumer",
        "Origin": "https://web.vodafone.com.eg"
    }
    payload = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "createdBy": {"value": "MobileApp"},
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [{"characteristicName": "quotaDist1", "type": "percentage", "value": quota}]
            },
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": user_data[user_id]['number']}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": member2}], "type": "Member"}
            ]
        },
        "type": "QuotaRedistribution"
    }
    
    try:
        response = session.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return True
        else:
            context.bot.send_message(chat_id=user_id, text=f"⚠️ خطأ في الفرد الثاني: {response.text}")
            return False
    except Exception as e:
        context.bot.send_message(chat_id=user_id, text=f"❌ خطأ اتصال بالفرد الثاني: {str(e)}")
        return False

def run_process(update: Update, context: CallbackContext) -> None:
    """تنفيذ العملية الرئيسية"""
    query = update.callback_query
    user_id = query.from_user.id
    if user_id not in allowed_users and user_id != ADMIN_ID:
        query.edit_message_text("❌ غير مصرح لك باستخدام هذه الخاصية.")
        return
    
    query.answer()
    if user_id not in user_data or user_data[user_id]['step'] != 'confirm':
        query.edit_message_text(text="⚠️ لم يتم إعداد البيانات بشكل صحيح. الرجاء البدء من جديد باستخدام /start")
        return
    
    query.edit_message_text(text="⏳ جاري بدء العملية...")
    data = user_data[user_id]
    total_attempts = data['attempts']
    successful_attempts = 0
    
    for attempt in range(1, total_attempts + 1):
        success = execute_attempt(user_id, attempt, total_attempts, context)
        if success:
            successful_attempts += 1
        time.sleep(10)
    
    # تحديث إحصائيات الاستخدام
    today = str(date.today())
    if user_id in usage_stats and usage_stats[user_id]['date'] == today:
        usage_stats[user_id]['count'] += 1
    else:
        usage_stats[user_id] = {'date': today, 'count': 1}
    save_data(allowed_users, usage_stats)
    
    summary = f"""
    🏁 النتائج النهائية:
    عدد المحاولات: {total_attempts}
    المحاولات الناجحة: {successful_attempts}
    نسبة النجاح: {round((successful_attempts/total_attempts)*100, 2)}%
    يمكنك البدء من جديد باستخدام /start
    """
    context.bot.send_message(chat_id=user_id, text=summary)
    
    if user_id in user_data:
        del user_data[user_id]

def cancel_process(update: Update, context: CallbackContext) -> None:
    """إلغاء العملية"""
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    
    if user_id in user_data:
        del user_data[user_id]
    query.edit_message_text(text="❌ تم إلغاء العملية. يمكنك البدء من جديد باستخدام /start")

def main() -> None:
    """تشغيل البوت"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # تعريف handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("allow", allow_user))
    dispatcher.add_handler(CommandHandler("disallow", disallow_user))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CallbackQueryHandler(start_process, pattern='^start_process$'))
    dispatcher.add_handler(CallbackQueryHandler(run_process, pattern='^run_process$'))
    dispatcher.add_handler(CallbackQueryHandler(cancel_process, pattern='^cancel_process$'))
    dispatcher.add_handler(CallbackQueryHandler(show_stats, pattern='^show_stats$'))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()