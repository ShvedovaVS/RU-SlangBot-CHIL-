import pytest


@pytest.mark.logic
class TestBotLogic:

    def test_exact_match(self, bot):
        result = bot.analyzer.find_words("Это кайф")
        assert "кайф" in result

    def test_case_insensitive(self, bot):
        result = bot.analyzer.find_words("ХАЙП")
        assert "хайп" in result

    def test_stem_match(self, bot):
        result = bot.analyzer.find_words("пруфы")
        assert "пруф" in result

    def test_substring_match(self, bot):
        result = bot.analyzer.find_words("мегахайповый")
        assert "хайп" in result

    def test_no_match(self, bot):
        result = bot.analyzer.find_words("привет мир")
        assert result == {}

    def test_multiple_words(self, bot):
        result = bot.analyzer.find_words("это был хайп но нет пруфов")
        assert "хайп" in result and "пруф" in result
