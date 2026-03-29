import asyncio

try:
    from .slang_bot import Bot
except ImportError:
    from slang_bot import Bot

if __name__ == "__main__":
    bot = Bot()

    # Запускаем асинхронную функцию
    asyncio.run(bot.run())
