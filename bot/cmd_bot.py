from module.cmd.konlpy_lib import Konlpy
from module.cmd.parser import Parser


class CMDBot:
    def __init__(self):
        self.cmd_commander = Konlpy()
        self.cmd_parser = Parser()

    def get_command(self, sentence):
        nouns = self.cmd_commander.get_nouns(sentence)
        return nouns

    def parse_sentence(self, sentence):
        spoken_part, command_list = self.cmd_parser.parse_sentence_with_commands(
            sentence
        )
        if "False" in spoken_part:
            return "다시 말씀해주세요", command_list
        return spoken_part, command_list
