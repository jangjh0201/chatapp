from konlpy.tag import Okt


class Konlpy:
    def __init__(self):
        self.okt = Okt()

    def __str__(self):
        return self.__class__.__name__

    def get_nouns(self, text):
        # return self.okt.nouns(text)

        pos_result = self.okt.pos(text)
        keywords = [
            word for word, pos in pos_result if pos in ["Noun", "Adjective", "Verb"]
        ]
        return keywords
