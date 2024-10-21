import re


class Parser:
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def parse_sentence_with_commands(self, sentence: str):
        """
        문장에서 구어체 부분과 대괄호 안에 있는 명령어 리스트를 분리합니다.

        Args:
            sentence (str): 구어체와 명령어 리스트가 포함된 문장

        Returns:
            tuple: (구어체 문장, 명령어 리스트)
        """
        # 정규 표현식을 사용하여 문장 끝에 있는 [] 부분을 추출
        match = re.search(r"\[(.*?)\]$", sentence)

        if match:
            # 구어체 문장은 대괄호 이전 부분을 가져옴
            spoken_part = sentence[: match.start()].strip()
            # 명령어 리스트는 대괄호 안의 내용을 쉼표 기준으로 분리
            command_list = match.group(1).split(",")
            # 명령어 리스트의 각 항목에서 불필요한 공백 제거
            command_list = [cmd.strip() for cmd in command_list]
            return spoken_part, command_list
        else:
            # 대괄호가 없는 경우, 전체 문장을 구어체로 반환하고 빈 명령어 리스트 반환
            return sentence, []
