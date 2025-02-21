TELEGRAM_TOKEN = "7695074963:AAHx1HrkMbUDA_dJ_yT60cAmL0isQaIrLsA"
import openai
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Настройки проксиjj
proxy_host = '216.173.107.26'
proxy_port = '5994'
proxies = {
    'http': f'http://{proxy_host}:{proxy_port}',
}


async def ask_gpt(prompt):
    """Функция для отправки запроса в GPT-4o."""
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
        json={
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "Ты — AI-бот, отвечающий на вопросы о Латокен и Хакатоне."},
                {"role": "user", "content": prompt}
            ]
        },
        proxies=proxies
    )
    print(response.json())
    return response.json()['choices'][0]['message']['content']

async def handle_message(update: Update, context: CallbackContext):
    """Обработчик текстовых сообщений."""
    user_message = update.message.text
    response = await ask_gpt(user_message)
    await update.message.reply_text(response)

async def main():
    """Основная функция запуска бота."""
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчик сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    await app.run_polling()

import asyncio
import nest_asyncio
nest_asyncio.apply()
async def start():
    await main()

if __name__ == "__main__":
    asyncio.run(start())
