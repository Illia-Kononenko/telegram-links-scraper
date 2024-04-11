import re
from telethon import TelegramClient, events, sync
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Создание клиента
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Подключение к клиенту
    await client.start()

    while True:
        # Ввод пользователя: введите URL группы или "exit" для выхода
        group_link = input("Введите ссылку на группу Telegram или 'exit' для выхода: ")
        if group_link.lower() == 'exit':
            print("Выход из программы.")
            break

        # Переход в группу по ссылке
        group = await client.get_entity(group_link)

        # Получение последних 100 сообщений
        messages = await client.get_messages(group, limit=100)

        # Регулярное выражение для поиска URL
        url_pattern = re.compile(r'(?:https?:)?\/\/(?:t(?:elegram)?\.me|telegram\.org)\/(?P<username>[a-z0-9\_]{5,32})\/?')

        # Набор для хранения уникальных URL
        unique_urls = set()

        # Проход по сообщениям и извлечение ссылок
        for message in messages:
            if message.text:
                urls = url_pattern.findall(message.text)
                for url in urls:
                    unique_urls.add(url.strip(')'))

        # Анализ типа сущностей по каждой уникальной ссылке
        for url in unique_urls:
            try:
                entity = await client.get_entity(url)
                print(f"Found URL: https://t.me/{url}, Type: {entity.__class__.__name__}, Title: {getattr(entity, 'title', '')}")
            except Exception as e:
                print(f"Failed to retrieve entity for URL: https://t.me/{url}, Error: {str(e)}")

# Запуск клиента и выполнение функции main
with client:
    client.loop.run_until_complete(main())
