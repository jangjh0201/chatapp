from module.cmd.konlpy_lib import Konlpy


class CMDBot:
    def __init__(self):
        self.konlpy = Konlpy()

    def get_command(self, sentence):
        nouns = self.konlpy.get_nouns(sentence)
        return nouns
