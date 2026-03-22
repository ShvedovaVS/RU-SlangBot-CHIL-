from bot.word_stemmer import Stemmer


class TestStemmer:

    def setup_method(self):
        """Создается перед каждым тестом"""
        self.stemmer = Stemmer()

    def test_lowercase(self):
        """Слово приводится к нижнему регистру"""
        assert self.stemmer.stem_russian("КРИНЖ") == "кринж"

    def test_remove_prefix(self):
        """Удаление префикса"""
        result = self.stemmer.stem_russian("забуллить")
        assert result != "буллить"

    def test_remove_suffix(self):
        """Удаление суффикса/окончания"""
        assert self.stemmer.stem_russian("токсики") == "токсик"

    def test_simple_word(self):
        """Простое слово обрабатывается"""
        assert self.stemmer.stem_russian("фейс") == "фейс"

    def test_complex_word(self):
        """Сложное слово обрабатывается"""
        assert self.stemmer.stem_russian("порофлит") == "рофл"
