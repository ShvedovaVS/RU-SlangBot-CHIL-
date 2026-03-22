import pytest


@pytest.mark.stemmer
class TestStemmer:

    def test_lowercase(self, stemmer):
        assert stemmer.stem_russian("КРИНЖ") == "кринж"

    def test_remove_suffix(self, stemmer):
        assert stemmer.stem_russian("токсики") == "токсик"

    def test_simple_word(self, stemmer):
        assert stemmer.stem_russian("фейс") == "фейс"

    def test_complex_word(self, stemmer):
        assert stemmer.stem_russian("порофлит") == "рофл"
