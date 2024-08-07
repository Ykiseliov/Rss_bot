import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telethon import TelegramClient, events

# Установите параметры вашего бота и клиента
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Список каналов для отслеживания
channels = []


# Функция для старта бота
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, который собирает посты из каналов. Используй /add для добавления канала.')


# Функция для добавления канала
def add_channel(update: Update, context: CallbackContext) -> None:
    if context.args:
        channel = context.args[0]
        channels.append(channel)
        update.message.reply_text(f'Канал {channel} добавлен для отслеживания.')
    else:
        update.message.reply_text('Пожалуйста, укажите название канала.')


# Функция для получения постов из каналов
async def fetch_posts():
    async with TelegramClient('bot', API_ID, API_HASH) as client:
        while True:
            for channel in channels:
                async for message in client.iter_messages(channel, limit=1):
                    # Отправляем сообщение в Telegram-бот
                    await bot.send_message(chat_id='YOUR_CHAT_ID', text=message.text)
            await asyncio.sleep(60)  # Пауза между запросами


# Основная функция
def main():
    # Создаем бота
    updater = Updater(BOT_TOKEN)

    # Получаем диспетчер
    dp = updater.dispatcher

    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_channel))

    # Запускаем бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    import asyncio
    from telegram import Bot

    # Инициализируем бота
    bot = Bot(token=BOT_TOKEN)

    # Запускаем асинхронную задачу для получения постов
    asyncio.run(fetch_posts())

    # Запускаем основной цикл бота
    main()