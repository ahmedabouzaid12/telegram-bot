from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import BotCommand, Update
from telegram.ext import CallbackContext
from handlers import start, button, handle_message
import logging
import requests  # أضفت ده عشان نستخدم requests.Timeout في error_handler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def set_bot_commands(application):
    commands = [
        BotCommand("start", "بدء تشغيل البوت")
    ]
    await application.bot.set_my_commands(commands)

async def error_handler(update: Update, context: CallbackContext) -> None:
    error = context.error
    logger.error(f"Error: {error}", exc_info=True)
    if update:
        if isinstance(error, requests.Timeout):
            await update.effective_chat.send_message(
                text="❌ انتهى وقت الطلب! السيرفر بطيء جدًا، جرب تاني بعد شوية أو تأكد من الاتصال بالإنترنت."
            )
        else:
            await update.effective_chat.send_message(
                text=f"❌ حصل خطأ أثناء معالجة طلبك: {str(error)}\nيرجى المحاولة مرة أخرى أو التواصل مع الدعم."
            )

def main():
    try:
        # Replace with your actual token
        token = "7615179073:AAGYJq5X8MmWULNegRNPE7s9Ql77o17myqE"
        
        # Test the token by printing bot info (debugging)
        logger.info("Testing bot token...")
        application = Application.builder().token(token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        # Set bot commands
        application.post_init = set_bot_commands
        
        logger.info("✅ البوت شغال يا معلم، مستني الأوامر!")
        application.run_polling()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)

if __name__ == '__main__':
    main()