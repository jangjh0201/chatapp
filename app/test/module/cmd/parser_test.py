import pytest
from app.module.cmd.parser import Parser  # Parser 클래스를 작성한 모듈에서 가져옵니다.


@pytest.fixture
def parser():
    """Parser 객체를 반환하는 fixture"""
    return Parser()


def test_parse_with_commands(parser):
    """명령어 리스트가 포함된 문장을 테스트"""
    sentence = "시원한 음료는 아이스티가 있어요. 아이스티를 만들어드릴까요? [시원한, 아이스티, 만들기]"
    expected_spoken_part = "시원한 음료는 아이스티가 있어요. 아이스티를 만들어드릴까요?"
    expected_command_list = ["시원한", "아이스티", "만들기"]

    spoken_part, command_list = parser.parse_sentence_with_commands(sentence)

    assert spoken_part == expected_spoken_part
    assert command_list == expected_command_list


def test_parse_without_commands(parser):
    """명령어 리스트가 포함되지 않은 문장을 테스트"""
    sentence = "안녕하세요. 오늘 날씨가 좋네요."
    expected_spoken_part = "안녕하세요. 오늘 날씨가 좋네요."
    expected_command_list = []

    spoken_part, command_list = parser.parse_sentence_with_commands(sentence)

    assert spoken_part == expected_spoken_part
    assert command_list == expected_command_list


def test_parse_empty_brackets(parser):
    """빈 명령어 리스트가 포함된 문장을 테스트"""
    sentence = "무엇을 도와드릴까요? []"
    expected_spoken_part = "무엇을 도와드릴까요?"
    expected_command_list = []

    spoken_part, command_list = parser.parse_sentence_with_commands(sentence)

    assert spoken_part == expected_spoken_part
    assert command_list == expected_command_list
