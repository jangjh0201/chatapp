from konlpy.tag import Okt


class Konlpy:
    def __init__(self):
        pass

    def get_nouns(self, text):
        okt = Okt()
        return okt.nouns(text)
