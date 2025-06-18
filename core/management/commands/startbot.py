# models/management/commands/startbot.py

import logging
from decouple import config
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async

from core.models import UserModel

BOT_TOKEN = config("BOT_TOKEN", default=None)
CHAT_ID = config("CHAT_ID", default=None)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Assalomu alaykum, {user.mention_html()}!\n\n"
        f"Men xodimlarning ishga kelib-ketishini nazorat qilaman.\n"
        f"Ruxsat etilgan guruhda kimlar ishda ekanligini bilish uchun /status komandasini yuboring."
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not CHAT_ID:
        logger.warning(
            "CHAT_ID muhit o'zgaruvchisi (.env faylda) o'rnatilmagan. Xavfsizlik uchun /status komandasi o'chirildi.")
        return

    incoming_chat_id = str(update.message.chat.id)
    allowed_chat_id = str(CHAT_ID)

    if incoming_chat_id != allowed_chat_id:
        logger.info(f"Ruxsat etilmagan chatdan (ID: {incoming_chat_id}) /status komandasi chaqirildi.")
        return

    try:
        @sync_to_async
        def get_all_users_from_db():
            return list(UserModel.objects.all().order_by('full_name'))

        users = await get_all_users_from_db()

        if not users:
            await update.message.reply_text("Tizimda hali birorta ham foydalanuvchi ro'yxatdan o'tmagan.")
            return

        at_work = []
        not_at_work = []

        for user in users:
            user_display = user.full_name or f"Nomsiz (ID: {user.user})"
            if user.status:
                at_work.append(f"✅ {user_display}")
            else:
                not_at_work.append(f"❌ {user_display}")

        message_parts = []

        if at_work:
            message_parts.append("🏢 **Ish joyida:**")
            message_parts.append("\n".join(at_work))
        else:
            message_parts.append("🏢 **Ish joyida:**\nHech kim ishda emas.")

        message_parts.append("\n" + "=" * 20 + "\n")

        if not_at_work:
            message_parts.append("🚶 **Ishda emas:**")
            message_parts.append("\n".join(not_at_work))
        else:
            message_parts.append("🚶 **Ishda emas:**\nHamma ish joyida.")

        final_message = "\n".join(message_parts)

        await update.message.reply_text(final_message, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"/status komandasini bajarishda xatolik yuz berdi: {e}")
        await update.message.reply_text(
            "Statusni olishda serverda xatolik yuz berdi. Iltimos, administratorga murojaat qiling.")


class Command(BaseCommand):
    help = 'Telegram botni ishga tushiradi'

    def handle(self, *args, **options):
        if not BOT_TOKEN:
            self.stdout.write(self.style.ERROR('BOT_TOKEN muhit o\'zgaruvchisida (.env faylda) topilmadi!'))
            return

        if not CHAT_ID:
            self.stdout.write(
                self.style.WARNING('Diqqat: CHAT_ID muhit o\'zgaruvchisi topilmadi. /status komandasi ishlamaydi.'))

        self.stdout.write(self.style.SUCCESS('Bot ishga tushirilmoqda... (To\'xtatish uchun CTRL+C)'))

        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("status", status_command))

        application.run_polling()