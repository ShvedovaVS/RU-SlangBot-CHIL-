import asyncio
import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from stemmer import stem_russian

from config import BOT_TOKEN

URL = "https://slovar-slenga.tilda.ws/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def fetch_page_with_retry(session, url, max_retries=3):
    """
    Загружает страницу
    """
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                wait_time = random.uniform(2, 5)
                print(f"⏳ Попытка {attempt + 1}...")
                sleep(wait_time)

            with session.get(url, timeout=30) as response:
                if response.status_code == 200:
                    return response.text
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
    return None


def parse_words_from_html(html):
    """
    Парсит слова, сохраняя многострочные значения
    """
    soup = BeautifulSoup(html, 'html.parser')
    words_data = {}

    text_blocks = soup.find_all('div', class_=re.compile(r't-text.*t-text_md'))
    print(f"📑 Найдено блоков: {len(text_blocks)}")

    total_found = 0

    for block in text_blocks:
        # Получаем HTML содержимое
        block_html = str(block)

        # Разбиваем по <br/> тегам
        lines = re.split(r'<br\s*/?>', block_html)

        current_word = None
        current_meaning = []

        for line in lines:
            # Удаляем HTML теги
            clean_line = re.sub(r'<[^>]+>', ' ', line).strip()

            if not clean_line or re.match(r'^[А-Я]\.\.\.', clean_line):
                continue

            # Проверяем, начинается ли строка с жирного слова
            bold_match = re.match(r'<strong>([^<]+)</strong>', line)

            if bold_match:
                # Если уже собирали предыдущее слово - сохраняем
                if current_word and current_meaning:
                    full_meaning = '\n'.join(current_meaning)
                    words_data.update({current_word: full_meaning})

                # Начинаем новое слово
                current_word = bold_match.group(1).strip().lower()
                current_meaning = []

                # Ищем значение после жирного слова в той же строке
                rest = line.replace(f"<strong>{bold_match.group(1)}</strong>", "").strip()
                if rest:
                    # Убираем тире в начале
                    rest = re.sub(r'^[-–—]\s*', '', rest)
                    if rest:
                        current_meaning.append(rest)

            elif current_word and clean_line:
                # Это продолжение значения
                # Убираем нумерацию типа "1)", "2)" в начале строки
                clean_line = re.sub(r'^\d+\)\s*', '', clean_line)
                current_meaning.append(clean_line)

        # Сохраняем последнее слово в блоке
        if current_word and current_meaning:
            full_meaning = '\n'.join(current_meaning)
            words_data.update({current_word: full_meaning})

    print(f"📊 Всего найдено: {len(words_data)} слов")
    return words_data


# --- Парсинг словаря с сайта ---
def import_from_site():
    with requests.Session() as session:
        session.headers.update(HEADERS)
        html = fetch_page_with_retry(session, URL)

        if not html:
            print("❌ Не удалось загрузить сайт")
            return

        words = parse_words_from_html(html)

        if not words:
            print("❌ Слова не найдены")
            return

        return words


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот-словарь сленга\n\n"
        "📝 Отправь мне сообщение, и я найду в нем сленговые слова и дам их объяснения.\n\n"
        "📚 Словарь содержит основные сленговые выражения.\n"
        "🔍 Пример: 'Вчера был такой кринж, просто зашквар!'"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    words = re.findall(r'\b[а-яёa-z]+\b', text, re.IGNORECASE)

    found_words = {}
    for word in words:
        if word in SLANG_DICT:
            found_words[word] = SLANG_DICT[word]
        else:
            # Приводим к корню
            stem = stem_russian(word)
            if stem in SLANG_DICT:
                found_words[stem] = SLANG_DICT[stem]
            else:
                # Поиск по вхождению
                for slang_word in SLANG_DICT:
                    if len(slang_word) > 2 and slang_word in word:
                        found_words[slang_word] = SLANG_DICT[slang_word]
                        break

    if not found_words:
        await update.message.reply_text(
            "😔 Сленговых слов не найдено\n\n"
            "💡 Попробуй другие слова или напиши /words для просмотра словаря"
        )
        return

    response = "🔍 *Найденные сленговые слова:*\n\n"
    for word, definition in found_words.items():
        response += f"• *{word}* — {definition}\n"

    await update.message.reply_text(response, parse_mode='Markdown')


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 *Статистика словаря*\n\n"
        f"📚 Всего слов: *{len(SLANG_DICT)}*\n"
        f"🔤 Язык: русский\n"
        f"📖 Источник: Илели, А. Толковый словарь русского молодёжного сленга / А. Илели, А. Федотова. – [Б. м.] : "
        f"Tilda Publishing, 2025. – URL: https://slovar-slenga.tilda.ws/ (дата обращения: 20.03.2026).\n",
        parse_mode='Markdown'
    )


async def show_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Показывает список всех слов в словаре
    """
    words_list = sorted(list(SLANG_DICT.keys()))

    # Разбиваем на части по 50 слов
    chunks = [words_list[i:i + 50] for i in range(0, len(words_list), 50)]

    for i, chunk in enumerate(chunks):
        response = f"📚 *Словарь сленга (часть {i + 1}/{len(chunks)}):*\n\n"
        response += ", ".join([f"*{word}*" for word in chunk])

        if i == 0:
            response += "\n\n💡 Чтобы узнать значение слова, просто отправь его в чат!"

        await update.message.reply_text(response, parse_mode='Markdown')


async def main():
    """
    Главная функция для запуска бота
    """
    global SLANG_DICT

    # Загружаем словарь
    print("📚 Загрузка словаря...")
    SLANG_DICT = import_from_site()

    print(f"✅ Готово")

    # Токен бота (в файле конфигурации, скрытым по соображениям безопасности)
    TOKEN = BOT_TOKEN

    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("words", show_words))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

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


if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())
