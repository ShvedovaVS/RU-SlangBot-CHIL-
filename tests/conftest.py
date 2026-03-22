import pytest
from bot.slang_bot import Bot
from bot.word_stemmer import Stemmer
from bot.site_parser import Parser


@pytest.fixture
def stemmer():
    return Stemmer()


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def bot():
    bot = Bot()
    bot.slang_dict = {
        "кайф": "удовольствие",
        "хайп": "ажиотаж",
        "пруф": "доказательство"
    }
    return bot
