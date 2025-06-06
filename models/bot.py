import requests
from decouple import config
from django.conf import settings

BOT_TOKEN = config("BOT_TOKEN", default=None)
CHAT_ID = config("CHAT_ID", default=None)


def send_message_to_telegram(come_gone_instance):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram sozlamalari (BOT_TOKEN yoki CHAT_ID) topilmadi.")
        if getattr(settings, 'DEBUG', False):  # DEBUG ni xavfsiz olish
            pass
        return

    try:
        user_model = come_gone_instance.user
        full_name = user_model.full_name if user_model.full_name else f"ID: {user_model.user}"
        event_time = come_gone_instance.time.strftime("%d-%m-%Y %H:%M:%S")
        event_status_text = "#Keldi ✅" if come_gone_instance.status else "#Ketdi 🚪"
        user_status_text = 'Ish joyida' if user_model.status else 'Ish joyida emas'

        text = (
            f"{event_status_text}\n"
            f"👤 **F.I.O:** {full_name}\n"
            f"🕒 **Vaqt:** {event_time}\n"
            f"🏢 **Holati:** {user_status_text}"
        )

        payload = {
            'chat_id': CHAT_ID,
            'text': text,
            'parse_mode': 'Markdown'
        }

        api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        response = requests.post(api_url, data=payload, timeout=10)
        response.raise_for_status()

        response_json = response.json()
        if response_json.get('ok'):
            print(
                f"Telegramga xabar muvaffaqiyatli yuborildi. Message ID: {response_json.get('result', {}).get('message_id')}")
        else:
            print(f"Telegramga xabar yuborildi, lekin 'ok' statusi false: {response_json}")

    except requests.exceptions.Timeout:
        print(f"Telegram API ga so'rov yuborishda timeout (10s).")
    except requests.exceptions.HTTPError as http_err:
        print(f"Telegram API dan HTTP xatolik: {http_err} - Javob: {http_err.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Telegram API ga ulanishda xatolik: {e}")
    except Exception as e:
        print(
            f"Telegramga xabar yuborishda kutilmagan xatolik: {e}, Javob matni (agar mavjud bo'lsa): {getattr(e, 'response', 'N/A')}")