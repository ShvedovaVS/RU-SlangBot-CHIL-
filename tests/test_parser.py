import pytest


@pytest.mark.parser
class TestParser:

    def test_empty_html(self, parser):
        assert parser.parse_words_from_html("") == {}

    def test_no_words(self, parser):
        html = "<div>Просто текст</div>"
        assert parser.parse_words_from_html(html) == {}
