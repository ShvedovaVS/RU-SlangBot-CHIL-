import random
import re
from time import sleep
from typing import Optional

import requests
from bs4 import BeautifulSoup


class Parser:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36'
    }

    URL = "https://slovar-slenga.tilda.ws/"

    def parse_words_from_html(self, html: str) -> dict:
        """
        Парсит слова, сохраняя многострочные значения

        Args:
            html: HTML страницы

        Returns:
            dict: Словарь {слово: определение}
        """
        soup = BeautifulSoup(html, 'html.parser')
        words_data = {}

        text_blocks = soup.find_all(
            'div', class_=re.compile(r't-text.*t-text_md'))
        print(f"📑 Найдено блоков: {len(text_blocks)}")

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
                        words_data[current_word] = full_meaning

                    # Начинаем новое слово
                    current_word = bold_match.group(1).strip().lower()
                    current_meaning = []

                    # Ищем значение после жирного слова в той же строке
                    rest = line.replace(f"<strong>{bold_match.group(1)}"
                                        f"</strong>", "").strip()
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
                words_data[current_word] = full_meaning

        print(f"📊 Всего найдено: {len(words_data)} слов")
        return words_data

    def import_from_site(self) -> Optional[dict]:
        """
        Импортирует слова с сайта

        Returns:
            Optional[dict]: Словарь слов или None в случае ошибки
        """
        with requests.Session() as session:
            session.headers.update(self.HEADERS)
            html = self.fetch_page_with_retry(session, self.URL)

            if not html:
                print("❌ Не удалось загрузить сайт")
                return None

            words = self.parse_words_from_html(html)

            if not words:
                print("❌ Слова не найдены")
                return None

            return words

    def fetch_page_with_retry(self, session, url: str, max_retries: int = 3) -> Optional[str]:
        """
        Загружает страницу с повторными попытками

        Args:
            session: requests.Session объект
            url: URL страницы
            max_retries: максимальное количество попыток

        Returns:
            Optional[str]: HTML страницы или None если не удалось загрузить
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
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"⚠️ Ошибка: {e}")

        return None
