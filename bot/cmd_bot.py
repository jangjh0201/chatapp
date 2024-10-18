from module.cmd.konlpy_lib import Konlpy


class CMDBot:
    def __init__(self):
        self.cmd_module = Konlpy()

    def get_command(self, sentence):
        nouns = self.cmd_module.get_nouns(sentence)
        return nouns
