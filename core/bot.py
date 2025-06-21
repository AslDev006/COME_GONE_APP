import requests
from decouple import config
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

BOT_TOKEN = config("BOT_TOKEN", default=None)
CHAT_ID = config("CHAT_ID", default=None)


def _send_telegram_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        logger.error("Telegram sozlamalari (BOT_TOKEN yoki CHAT_ID) .env faylida topilmadi.")
        return

    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    try:
        response = requests.post(api_url, data=payload, timeout=10)
        response.raise_for_status()
        logger.info("Telegramga xabar muvaffaqiyatli yuborildi.")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Telegram API dan HTTP xatolik: {http_err} - Javob: {http_err.response.text}", exc_info=True)
    except Exception as e:
        logger.error(f"Telegramga xabar yuborishda kutilmagan xatolik: {e}", exc_info=True)


def send_message_to_telegram(come_gone_instance):
    user_model = come_gone_instance.user
    full_name = user_model.full_name or f"ID: {user_model.user}"
    local_time = timezone.localtime(come_gone_instance.time)
    event_time = local_time.strftime("%d-%m-%Y %H:%M:%S")
    event_status_text = "#Keldi ✅" if come_gone_instance.status else "#Ketdi 🚪"
    user_status_text = 'Ish joyida' if user_model.status else 'Ish joyida emas'

    text = (
        f"{event_status_text}\n"
        f"👤 **F.I.O:** {full_name}\n"
        f"🕒 **Vaqt:** {event_time}\n"
        f"🏢 **Holati:** {user_status_text}"
    )
    _send_telegram_message(text)


def send_auto_checkout_message(come_gone_instance):
    user_model = come_gone_instance.user
    full_name = user_model.full_name or f"ID: {user_model.user}"
    local_time = timezone.localtime(come_gone_instance.time)
    event_time = local_time.strftime("%d-%m-%Y %H:%M:%S")

    text = (
        f"#AvtomatikChiqish ⚙️\n\n"
        "Diqqat! Xodim tizimdan chiqishni unutganligi sababli, kun yakunida "
        "avtomatik ravishda tizimdan chiqarildi.\n\n"
        f"👤 **F.I.O:** {full_name}\n"
        f"🕒 **Chiqish vaqti:** {event_time}\n"
        f"🏢 **Holati:** Ish joyida emas"
    )
    _send_telegram_message(text)