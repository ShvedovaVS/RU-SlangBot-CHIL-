from bot.slang_bot import Bot


class TestBotLogic:

    def setup_method(self):
        """Создаем тестовый бот"""
        self.bot = Bot()
        self.bot.slang_dict = {
            "кайф": "удовольствие",
            "хайп": "ажиотаж",
            "пруф": "доказательство"
        }

    def test_exact_match(self):
        """Точное совпадение"""
        result = self.bot.find_words("Это кайф")
        assert "кайф" in result

    def test_case_insensitive(self):
        """Независимость от регистра"""
        result = self.bot.find_words("ХАЙП")
        assert "хайп" in result

    def test_stem_match(self):
        """Поиск через стемминг"""
        result = self.bot.find_words("пруфы")
        assert "пруф" in result

    def test_substring_match(self):
        """Поиск по вхождению"""
        result = self.bot.find_words("мегахайповый")
        assert "хайп" in result

    def test_no_match(self):
        """Нет совпадений"""
        result = self.bot.find_words("привет мир")
        assert result == {}

    def test_multiple_words(self):
        """Несколько слов"""
        result = self.bot.find_words("это был хайп но нет пруфов")
        assert "хайп" in result and "пруф" in result
