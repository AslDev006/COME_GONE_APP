# models/management/commands/startbot.py
import logging
from decouple import config
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async
from core.models import UserModel
from core.utils import calculate_work_summary
from django.utils import timezone
from datetime import timedelta
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

async def work_time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not CHAT_ID or str(update.message.chat.id) != str(CHAT_ID):
        logger.info(f"Ruxsat etilmagan chatdan (ID: {update.message.chat.id}) /work_time chaqirildi.")
        return

    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    if not context.args:
        await update.message.reply_text("Barcha xodimlar uchun hisobot tayyorlanmoqda, iltimos kuting...")

        @sync_to_async
        def get_all_users_summaries(start_date, end_date):
            users = UserModel.objects.all().order_by('full_name')
            results = []
            for user in users:
                summary = calculate_work_summary(user, start_date, end_date)
                results.append({'user': user, 'summary': summary})
            return results

        all_summaries = await get_all_users_summaries(start_of_month, today)

        message_parts = [
            f"*{start_of_month.strftime('%B %Y')} oyi uchun umumiy hisobot*",
            f"_(Hisobot sanasi: {today.strftime('%d.%m.%Y')})_\n"
        ]

        if not all_summaries:
            message_parts.append("Tizimda hisobot uchun xodimlar topilmadi.")
        else:
            for item in all_summaries:
                user = item['user']
                summary = item['summary']

                total_seconds = summary['total_duration'].total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                days = summary['total_days']

                line = f"👤 *{user.full_name}* (ID: `{user.user}`): {days} kun | {hours} soat {minutes} daqiqa"
                message_parts.append(line)

        final_message = "\n".join(message_parts)
        await update.message.reply_text(final_message, parse_mode='Markdown')
        return

    try:
        user_id = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Iltimos, xodimning ID raqamini to'g'ri kiriting. Namuna: `/work_time 42`")
        return

    @sync_to_async
    def get_user_and_calculate(user_id, start_date, end_date):
        try:
            user = UserModel.objects.get(user=user_id)
        except UserModel.DoesNotExist:
            return None, None

        summary = calculate_work_summary(user, start_date, end_date)
        return user, summary

    user, summary = await get_user_and_calculate(user_id, start_of_month, today)

    if not user:
        await update.message.reply_text(f"Berilgan ID (`{user_id}`) bilan xodim topilmadi.")
        return

    total_seconds = summary['total_duration'].total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    total_days = summary['total_days']

    response_text = (
        f"👤 **Xodim:** {user.full_name} (ID: {user.user})\n"
        f"📅 **Hisobot davri:** {start_of_month.strftime('%d.%m.%Y')} - {today.strftime('%d.%m.%Y')}\n\n"
        f"🏢 **Jami ishlagan kun:** {total_days} kun\n"
        f"⏱ **Jami ishlagan vaqt:** {hours} soat, {minutes} daqiqa"
    )

    await update.message.reply_text(response_text, parse_mode='Markdown')

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
        application.add_handler(CommandHandler("work_time", work_time_command))
        application.run_polling()