import asyncio
import re

# pylint: disable=import-error, no-name-in-module
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# pylint: enable=import-error, no-name-in-module

import site_parser
import word_stemmer

try:
    from bot.config import BOT_TOKEN
except ImportError:
    BOT_TOKEN = None


class Bot:
    def __init__(self):
        self.slang_dict = {}
        self.stemmer = word_stemmer.Stemmer()
        self.parser = site_parser.Parser()

    async def start(self, update: Update, _context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "👋 Привет! Я бот-словарь сленга\n\n"
            "📝 Отправь мне сообщение, и я найду в нем "
            "сленговые слова и дам их объяснения.\n\n"
            "📚 Словарь содержит основные сленговые выражения.\n"
            "🔍 Пример: 'Вчера был такой кринж, просто зашквар!'"
        )

    async def help_command(self, update: Update, _context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 *Как пользоваться ботом:*\n\n"
            "1. Просто отправь любое сообщение\n"
            "2. Бот найдет все сленговые слова\n"
            "3. Получишь их объяснения\n\n"
            "*Команды:*\n"
            "/start - приветствие\n"
            "/help - эта справка\n"
            "/stats - статистика словаря\n"
            "/words - список всех слов\n\n"
            "*Пример:*\n"
            "«Вчера был кринж, просто хайп ловили!»",
            parse_mode='Markdown'
        )

    def find_words(self, text: str) -> dict:
        text = text.lower()
        words = re.findall(r'\b[а-яёa-z]+\b',
                           text, re.IGNORECASE)

        found_words = {}

        for word in words:
            if word in self.slang_dict:
                found_words[word] = self.slang_dict[word]
            else:
                stem = self.stemmer.stem_russian(word)
                if stem in self.slang_dict:
                    found_words[stem] = self.slang_dict[stem]
                else:
                    for slang_word, definition in self.slang_dict.items():
                        if len(slang_word) > 2 and slang_word in word:
                            found_words[slang_word] = definition
                            break

        return found_words

    async def handle_message(self, update: Update,
                             _context: ContextTypes.DEFAULT_TYPE):
        found_words = self.find_words(update.message.text)

        if not found_words:
            await update.message.reply_text(
                "😔 Сленговых слов не найдено\n\n"
                "💡 Попробуй другие слова или напиши "
                "/words для просмотра словаря"
            )
            return

        response = "🔍 *Найденные сленговые слова:*\n\n"
        for word, definition in found_words.items():
            response += f"• *{word}* — {definition}\n"

        await update.message.reply_text(response, parse_mode='Markdown')

    async def stats(self, update: Update, _context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"📊 *Статистика словаря*\n\n"
            f"📚 Всего слов: *{len(self.slang_dict)}*\n"
            f"🔤 Язык: русский\n"
            f"📖 Источник: Илели, А. Толковый словарь "
            f"русского молодёжного сленга / А. Илели, "
            f"А. Федотова. – [Б. м.] : "
            f"Tilda Publishing, 2025. – URL: "
            f"https://slovar-slenga.tilda.ws/ "
            f"(дата обращения: 20.03.2026).\n",
            parse_mode='Markdown'
        )

    async def show_words(self, update: Update, _context: ContextTypes.DEFAULT_TYPE):
        """
        Показывает список всех слов в словаре
        """
        words_list = sorted(list(self.slang_dict.keys()))

        # Разбиваем на части по 50 слов
        chunks = [words_list[i:i + 50]
                  for i in range(0, len(words_list), 50)]

        for i, chunk in enumerate(chunks):
            response = (f"📚 *Словарь сленга "
                        f"(часть {i + 1}/{len(chunks)}):*\n\n")
            response += ", ".join([f"*{word}*" for word in chunk])

            if i == 0:
                response += ("\n\n💡 Чтобы узнать значение слова, "
                             "просто отправь его в чат!")

            await update.message.reply_text(response, parse_mode='Markdown')

    async def run(self):
        """
        Главная функция для запуска бота
        """
        # Загружаем словарь
        print("📚 Загрузка словаря...")
        self.slang_dict = self.parser.import_from_site() or {}

        print("✅ Готово")

        # Токен бота
        token = BOT_TOKEN  # pylint: disable=invalid-name

        # Создаем приложение
        application = Application.builder().token(token).build()

        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats))
        application.add_handler(CommandHandler("words", self.show_words))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Запускаем бота
        print("🚀 Бот запущен...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        # Держим бота запущенным
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("👋 Остановка бота...")
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
