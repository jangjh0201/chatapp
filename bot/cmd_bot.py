from module.cmd.konlpy_lib import Konlpy
from module.cmd.parser import Parser
from module.cmd.converter import Converter


class CMDBot:
    def __init__(self):
        self.cmd_analyzer = Konlpy()
        self.cmd_parser = Parser()
        self.cmd_converter = Converter()

    def get_command(self, sentence):
        nouns = self.cmd_analyzer.get_nouns(sentence)
        return nouns

    def parse_sentence(self, sentence):
        spoken_part, command_list = self.cmd_parser.parse_sentence_with_commands(
            sentence
        )
        return spoken_part, command_list

    def create_response(self, command_list):
        return self.cmd_converter.convert(command_list)
