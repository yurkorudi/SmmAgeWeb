import asyncio
import html
import os

try:
    from aiogram import Bot
except ImportError:
    Bot = None


def _value(data, key):
    return html.escape(data.get(key) or "—")


def build_request_message(data):
    return (
        "<b>Нова заявка з сайту</b>\n\n"
        f"<b>Ім'я:</b> {_value(data, 'name')}\n"
        f"<b>Телефон:</b> {_value(data, 'phone')}\n"
        f"<b>Бізнес:</b> {_value(data, 'business')}\n"
        f"<b>Категорія:</b> {_value(data, 'category')}\n"
        f"<b>Бюджет:</b> {_value(data, 'budget')}\n"
        f"<b>Старт:</b> {_value(data, 'timeline')}\n\n"
        f"<b>Повідомлення:</b>\n{_value(data, 'message')}"
    )


async def _send_message(token, chat_id, text):
    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
    finally:
        await bot.session.close()


def notify_new_request(data):
    if Bot is None:
        print("Telegram notification skipped: install aiogram to enable bot notifications.")
        return

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id:
        print("Telegram notification skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is empty.")
        return

    try:
        asyncio.run(_send_message(token, chat_id, build_request_message(data)))
    except Exception as exc:
        print("Telegram notification error:", exc)
