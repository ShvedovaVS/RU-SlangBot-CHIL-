import asyncio

import slang_bot

if __name__ == "__main__":
    bot = slang_bot.Bot()

    # Запускаем асинхронную функцию
    asyncio.run(bot.run())
