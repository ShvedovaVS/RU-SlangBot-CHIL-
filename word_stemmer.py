class Stemmer:
    def stem_russian(self, word):
        """Приводит слово к корневой форме"""
        word = word.lower()

        # Приставки
        prefixes = ['за', 'на', 'по', 'при', 'от', 'до', 'с', 'у', 'в', 'вы', 'под', 'над', 'раз', 'рас', 'пере', 'про',
                    'об']

        # Суффиксы и окончания
        suffixes = [
            'ться', 'тся', 'ти', 'ть',  # глагольные
            'ет', 'ит', 'ат', 'ят', 'ут', 'ют',  # окончания
            'вш', 'вши', 'ш', 'ши',  # причастия
            'л', 'ла', 'ло', 'ли',  # прошедшее время
            'а', 'я', 'о', 'е', 'и', 'ы',  # падежные
            'ой', 'ей', 'ий', 'ый',  # прилагательные
            'ую', 'юю', 'ая', 'яя',
            'ие', 'ые', 'им', 'ым',
            'ем', 'ом', 'ам', 'ям',
            'у', 'ю'
        ]

        # Убираем приставку
        for prefix in prefixes:
            if word.startswith(prefix) and len(word) > len(prefix) + 2:
                word = word[len(prefix):]
                break

        # Убираем суффиксы
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                word = word[:-len(suffix)]
                break

        return word
