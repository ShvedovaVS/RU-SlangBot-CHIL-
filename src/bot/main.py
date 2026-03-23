import asyncio

from bot.slang_bot import Bot

if __name__ == "__main__":
    bot = Bot()

    # Запускаем асинхронную функцию
    asyncio.run(bot.run())
