import pytest
from bot.slang_bot import Bot
from bot.word_stemmer import Stemmer
from bot.site_parser import Parser
from bot.slang_analyzer import SlangAnalyzer

@pytest.fixture
def stemmer():
    return Stemmer()

@pytest.fixture
def parser():
    return Parser()

@pytest.fixture
def bot(stemmer):
    bot = Bot()
    bot.slang_dict = {
        "кайф": "удовольствие",
        "хайп": "ажиотаж",
        "пруф": "доказательство"
    }
    # инициализируем анализатор
    bot.analyzer = SlangAnalyzer(bot.slang_dict, stemmer)
    return bot
