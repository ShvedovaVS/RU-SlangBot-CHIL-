import re


class SlangAnalyzer:
    def __init__(self, slang_dict, stemmer):
        self.slang_dict = slang_dict
        self.stemmer = stemmer

    def find_words(self, text: str) -> dict:
        text = text.lower()
        words = re.findall(r'\b[а-яёa-z]+\b', text)

        found_words = {}

        for word in words:
            if word in self.slang_dict:
                found_words[word] = self.slang_dict[word]
                continue

            stem = self.stemmer.stem_russian(word)
            if stem in self.slang_dict:
                found_words[stem] = self.slang_dict[stem]
                continue

            for slang_word, definition in self.slang_dict.items():
                if len(slang_word) > 2 and slang_word in word:
                    found_words[slang_word] = definition
                    break

        return found_words
