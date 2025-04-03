from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from add_members import execute_vodafone_operations
from accept_requests import execute_accept_requests
from break_percentage import execute_break_percentage

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🟠 أورانج", callback_data='orange')],
        [InlineKeyboardButton("🟢 اتصالات", callback_data='etisalat')],
        [InlineKeyboardButton("🔴 فودافون", callback_data='vodafone')],
        [InlineKeyboardButton("🟣 وي", callback_data='we')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 مرحبًا بك في بوت MR MANDO 👾!\n\n"
        "🔹 هنا مكانك لو عايز أحدث وأفضل الاسكريبتات الخاصة بفودافون بكل سهولة وسرعة.\n"
        "🔹 هدفنا هو توفير حلول متكاملة وسهلة الاستخدام عشان نوفر عليك الوقت والمجهود.\n"
        "🔹 مع MR MANDO، هتلاقي أداء سريع، دعم مستمر، وتجربة استخدام ولا أروع! 💯\n\n"
        "🎯 اختر الخدمة اللي محتاجها من القوائم الجاهزة قدامك، وإحنا هنساعدك في كل خطوة! 💪🔥",
        reply_markup=reply_markup
    )

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    try:
        await query.answer()
    except BadRequest as e:
        if "query is too old" in str(e).lower():
            pass
        else:
            raise

    if query.data == "vodafone":
        vodafone_keyboard = [
            [InlineKeyboardButton("👥 إضافة فردين للعيلة", callback_data='individual_mod')],
            [InlineKeyboardButton("🎁 قبول طلبات الإضافة", callback_data='accept_requests')],
            [InlineKeyboardButton("💰 كسر النسبة", callback_data='break_percentage')],
            [InlineKeyboardButton("↩️ رجعني للقايمة الرئيسية", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(vodafone_keyboard)
        await query.edit_message_text(
            text="🚀مرحبًا بك في قسم فودافون! 🔴\n\n"
                 "🔹 هنا هتلاقي كل الخدمات والعروض الخاصة بفودافون بأسرع وأسهل طريقة.\n"
                 "🔹 اختار من القايمة اللي تحت واستمتع بأفضل المميزات اللي تهمك. 💡🔥\n\n"
                 "👇 اختار الخدمة اللي عايزها:",
            reply_markup=reply_markup
        )

    elif query.data == "individual_mod":
        context.user_data['step'] = 'family_owners_number'
        await query.edit_message_text(text="📞 ابعتلي رقم فودافون بتاع صاحب العيلة يا معلم!")

    elif query.data == "accept_requests":
        context.user_data['step'] = 'family_owners_number_accept'
        await query.edit_message_text(text="📞 ابعتلي رقم فودافون بتاع صاحب العيلة يا معلم!")

    elif query.data == "break_percentage":
        context.user_data['step'] = 'family_owners_number_break'
        await query.edit_message_text(text="📞 ابعتلي رقم فودافون بتاع صاحب العيلة يا معلم!")

    elif query.data == "back_to_vodafone":
        vodafone_keyboard = [
            [InlineKeyboardButton("👥 إضافة فردين للعيلة", callback_data='individual_mod')],
            [InlineKeyboardButton("🎁 قبول طلبات الإضافة", callback_data='accept_requests')],
            [InlineKeyboardButton("💰 كسر النسبة", callback_data='break_percentage')],
            [InlineKeyboardButton("↩️ رجعني للقايمة الرئيسية", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(vodafone_keyboard)
        await query.edit_message_text(
            text="🚀مرحبًا بك في قسم فودافون! 🔴\n\n"
                 "🔹 هنا هتلاقي كل الخدمات والعروض الخاصة بفودافون بأسرع وأسهل طريقة.\n"
                 "🔹 اختار من القايمة اللي تحت واستمتع بأفضل المميزات اللي تهمك. 💡🔥\n\n"
                 "👇 اختار الخدمة اللي عايزها:",
            reply_markup=reply_markup
        )

    elif query.data == "back_to_main":
        keyboard = [
            [InlineKeyboardButton("🟠 أورانج", callback_data='orange')],
            [InlineKeyboardButton("🟢 اتصالات", callback_data='etisalat')],
            [InlineKeyboardButton("🔴 فودافون", callback_data='vodafone')],
            [InlineKeyboardButton("🟣 وي", callback_data='we')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🚀 مرحبًا بك في بوت MR MANDO 👾!\n\n"
                 "🔹 هنا مكانك لو عايز أحدث وأفضل الاسكريبتات الخاصة بفودافون بكل سهولة وسرعة.\n"
                 "🔹 هدفنا هو توفير حلول متكاملة وسهلة الاستخدام عشان نوفر عليك الوقت والمجهود.\n"
                 "🔹 مع MR MANDO، هتلاقي أداء سريع، دعم مستمر، وتجربة استخدام ولا أروع! 💯\n\n"
                 "🎯 اختر الخدمة اللي محتاجها من القوائم الجاهزة قدامك، وإحنا هنساعدك في كل خطوة! 💪🔥",
            reply_markup=reply_markup
        )

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    user_data = context.user_data

    # لإضافة الأفراد (بس باسورد صاحب العيلة)
    if user_data.get('step') == 'family_owners_number':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['family_owners_number'] = user_input
        user_data['step'] = 'family_owners_password'
        await update.message.reply_text("🔐 ابعتلي باسورد أنا فودافون بتاع صاحب العيلة يا وحش!")
        return

    if user_data.get('step') == 'family_owners_password':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['family_owners_password'] = user_input
        user_data['step'] = 'member0'
        await update.message.reply_text("📱 ابعتلي رقم الفرد المضاف في العيلة مسبقًا يا كبير!")
        return

    if user_data.get('step') == 'member0':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member0'] = user_input
        user_data['step'] = 'member1'
        await update.message.reply_text("📲 ابعتلي رقم الفرد الأول اللي عايز تضيفه للعيلة يا نجم!")
        return

    if user_data.get('step') == 'member1':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member1'] = user_input
        user_data['step'] = 'member2'
        await update.message.reply_text("📳 ابعتلي رقم الفرد التاني اللي عايز تضيفه للعيلة يا معلم!")
        return

    

    if user_data.get('step') == 'member2':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member2'] = user_input

        message = (
            f"✅ تمام يا ريس! البيانات اللي دخلتها:\n"
            f"📞 رقم رب العيلة: {user_data['family_owners_number']}\n"
            f"🔐 باسورد رب العيلة: {user_data['family_owners_password']}\n"
            f"📱 الفرد المضاف مسبقًا: {user_data['member0']}\n"
            f"📲 الفرد الأول: {user_data['member1']}\n"
            f"📳 الفرد التاني: {user_data['member2']}\n\n"
            "🚀 جاري تنفيذ العمليات المطلوبة...\n"
            "⏳ ممكن ياخد شوية وقت، استنى معايا شوية..."
        )
        await update.message.reply_text(message)

        results = await execute_vodafone_operations(user_data.copy(), context)

        # التحقق من نتيجة إضافة الفرد الأول
        if "add_result1" in results:
            if "error" in results["add_result1"]:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"❌ حصل خطأ أثناء إضافة الفرد الأول: {results['add_result1']['error']}"
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="✅ تم إضافة الفرد الأول بنجاح!"
                )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ حصل خطأ غير متوقع أثناء إضافة الفرد الأول!"
            )

        # التحقق من نتيجة إضافة الفرد الثاني
        if "add_result2" in results:
            if "error" in results["add_result2"]:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"❌ حصل خطأ أثناء إضافة الفرد الثاني: {results['add_result2']['error']}"
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="✅ تم إضافة الفرد الثاني بنجاح!"
                )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ الفرد الثاني لم يتم إضافته بنجاح!"
            )

        user_data.clear()
        return

    # لقبول الطلبات (باسورد لكل فرد بما فيهم member0)
    if user_data.get('step') == 'family_owners_number_accept':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['family_owners_number'] = user_input
        user_data['step'] = 'family_owners_password_accept'
        await update.message.reply_text("🔐 ابعتلي باسورد أنا فودافون بتاع صاحب العيلة يا وحش!")
        return

    if user_data.get('step') == 'family_owners_password_accept':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['family_owners_password'] = user_input
        user_data['step'] = 'member0_accept'
        await update.message.reply_text("📱 ابعتلي رقم الفرد المضاف في العيلة مسبقًا يا كبير!")
        return

    if user_data.get('step') == 'member0_accept':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member0'] = user_input
        user_data['step'] = 'member0_password_accept'
        await update.message.reply_text("🔐 ابعتلي باسورد الفرد المضاف مسبقًا يا نجم!")
        return

    if user_data.get('step') == 'member0_password_accept':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['member0_password'] = user_input
        user_data['step'] = 'member1_accept'
        await update.message.reply_text("📲 ابعتلي رقم الفرد الأول اللي عايز تقبل دعوته يا نجم!")
        return

    if user_data.get('step') == 'member1_accept':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member1'] = user_input
        user_data['step'] = 'member1_password_accept'
        await update.message.reply_text("🔐 ابعتلي باسورد الفرد الأول يا كبير!")
        return

    if user_data.get('step') == 'member1_password_accept':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['member1_password'] = user_input
        user_data['step'] = 'member2_accept'
        await update.message.reply_text("📳 ابعتلي رقم الفرد التاني اللي عايز تقبل دعوته يا معلم!")
        return

    if user_data.get('step') == 'member2_accept':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member2'] = user_input
        user_data['step'] = 'member2_password_accept'
        await update.message.reply_text("🔐 ابعتلي باسورد الفرد التاني يا ريس!")
        return

    if user_data.get('step') == 'member2_password_accept':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['member2_password'] = user_input

        message = (
            f"✅ تمام يا ريس! البيانات اللي دخلتها:\n"
            f"📞 رقم رب العيلة: {user_data['family_owners_number']}\n"
            f"🔐 باسورد رب العيلة: {user_data['family_owners_password']}\n"
            f"📱 الفرد المضاف مسبقًا: {user_data['member0']}\n"
            f"🔐 باسورد الفرد المضاف: {user_data['member0_password']}\n"
            f"📲 الفرد الأول: {user_data['member1']}\n"
            f"🔐 باسورد الفرد الأول: {user_data['member1_password']}\n"
            f"📳 الفرد التاني: {user_data['member2']}\n"
            f"🔐 باسورد الفرد التاني: {user_data['member2_password']}\n\n"
            "🚀 جاري قبول طلبات الإضافة...\n"
            "⏳ ممكن ياخد شوية وقت، استنى معايا شوية..."
        )
        await update.message.reply_text(message)

        results = await execute_accept_requests(user_data.copy(), context)

        if "error" in results:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ حصل خطأ: {results['error']}"
            )
        else:
            success_message = (
                "🎉 تم قبول طلبات الإضافة بنجاح!\n\n"
                "✅ تم قبول دعوة الأفراد الجدد\n"
                "🔥 كل حاجة اتممت بنجاح يا كبير!"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=success_message
            )
        user_data.clear()
        return

    # لكسر النسبة (باسورد لكل فرد)
    if user_data.get('step') == 'family_owners_number_break':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['family_owners_number'] = user_input
        user_data['step'] = 'family_owners_password_break'
        await update.message.reply_text("🔐 ابعتلي باسورد أنا فودافون بتاع صاحب العيلة يا وحش!")
        return

    if user_data.get('step') == 'family_owners_password_break':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['family_owners_password'] = user_input
        user_data['step'] = 'member0_break'
        await update.message.reply_text("📱 ابعتلي رقم الفرد المضاف في العيلة مسبقًا يا كبير!")
        return

    if user_data.get('step') == 'member0_break':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member0'] = user_input
        user_data['step'] = 'member0_password_break'
        await update.message.reply_text("🔐 ابعتلي باسورد الفرد المضاف مسبقًا يا نجم!")
        return

    if user_data.get('step') == 'member0_password_break':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['member0_password'] = user_input
        user_data['step'] = 'member1_break'
        await update.message.reply_text("📲 ابعتلي رقم الفرد الأول اللي عايز تكسر نسبته يا نجم!")
        return

    if user_data.get('step') == 'member1_break':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member1'] = user_input
        user_data['step'] = 'member1_password_break'
        await update.message.reply_text("🔐 ابعتلي باسورد الفرد الأول يا كبير!")
        return

    if user_data.get('step') == 'member1_password_break':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['member1_password'] = user_input
        user_data['step'] = 'member2_break'
        await update.message.reply_text("📳 ابعتلي رقم الفرد التاني اللي عايز تكسر نسبته يا معلم!")
        return

    if user_data.get('step') == 'member2_break':
        if not user_input.isdigit() or len(user_input) != 11:
            await update.message.reply_text("⚠️ الرقم غير صحيح! يرجى إدخال رقم فودافون صحيح مكون من 11 رقم")
            return
        user_data['member2'] = user_input
        user_data['step'] = 'member2_password_break'
        await update.message.reply_text("🔐 ابعتلي باسورد الفرد التاني يا ريس!")
        return


    if user_data.get('step') == 'member2_password_break':
        if not user_input:
            await update.message.reply_text("⚠️ الباسورد لا يمكن أن يكون فارغًا!")
            return
        user_data['member2_password'] = user_input
        user_data['step'] = 'attempts_input'  # خطوة جديدة لإدخال عدد المحاولات
        await update.message.reply_text("🔄 كم عدد المحاولات اللي عايز تجربها؟ (الافتراضي: 30)")

    if user_data.get('step') == 'attempts_input':
        try:
            # إذا المستخدم ما دخلش رقم، نستخدم القيمة الافتراضية 30
            attempts = int(user_input) if user_input.strip() else 30
            if attempts <= 0:
                await update.message.reply_text("⚠️ عدد المحاولات لازم يكون أكبر من صفر!")
                return
            user_data['attempts'] = attempts
        except ValueError:
            await update.message.reply_text("⚠️ لازم تدخل رقم صحيح يا معلم!")
            return

        message = (
            f"✅ تمام يا ريس! البيانات اللي دخلتها:\n"
            f"📞 رقم رب العيلة: {user_data['family_owners_number']}\n"
            f"🔐 باسورد رب العيلة: {user_data['family_owners_password']}\n"
            f"📱 الفرد المضاف مسبقًا: {user_data['member0']}\n"
            f"🔐 باسورد الفرد المضاف: {user_data['member0_password']}\n"
            f"📲 الفرد الأول: {user_data['member1']}\n"
            f"🔐 باسورد الفرد الأول: {user_data['member1_password']}\n"
            f"📳 الفرد التاني: {user_data['member2']}\n"
            f"🔐 باسورد الفرد التاني: {user_data['member2_password']}\n"
            f"🔄 عدد المحاولات: {user_data['attempts']}\n\n"
            "🚀 جاري كسر النسبة...\n"
            "⏳ ممكن ياخد شوية وقت، استنى معايا شوية..."
        )
        await update.message.reply_text(message)

        results = await execute_break_percentage(user_data.copy(), context)

        if "error" in results:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ حصل خطأ: {results['error']}"
            )
        else:
            success_message = (
                "🎉 تم كسر النسبة بنجاح!\n\n"
                f"✅ عدد المحاولات المستخدمة: {results.get('attempts_used', 'غير معروف')}\n"
                "🔥 كل حاجة اتممت بنجاح يا كبير!"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=success_message
            )
        user_data.clear()
        return

# ... (بقية الكود تبقى كما هي)