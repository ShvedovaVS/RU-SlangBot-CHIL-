from bot.site_parser import Parser


class TestParser:

    def setup_method(self):
        self.parser = Parser()

    def test_empty_html(self):
        """Пустой HTML"""
        assert self.parser.parse_words_from_html("") == {}

    def test_no_words(self):
        """HTML без слов"""
        html = "<div>Просто текст</div>"
        assert self.parser.parse_words_from_html(html) == {}
