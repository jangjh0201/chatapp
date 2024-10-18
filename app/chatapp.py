from bot import cmd_bot, stt_bot, tts_bot


class ChatApp:
    def __init__(self):
        self.stt_bot = stt_bot.STTBot()
        self.cmd_bot = cmd_bot.CMDBot()
        self.tts_bot = tts_bot.TTSBot()

    def create_response(self, command_list):
        response = ""
        if "커피" in command_list or "아메리카노" in command_list:
            response = "커피를 만들어 드릴게요."
        elif "차" in command_list or "캐모마일" in command_list:
            response = "캐모마일 차를 만들어 드릴게요."
        elif "아이스티" in command_list:
            response = "아이스티를 만들어 드릴게요."
        elif "출근" in command_list:
            response = "출근 준비를 도와드릴게요."
        else:
            response = "이해하지 못했어요. 다시 말씀해 주세요."

        return response

    def run(self):
        # 음성 입력받기 (STT)
        sentence = self.stt_bot.listen()
        print(f"음성 입력: {sentence}")

        # 명령어 추출 (CMD)
        command_list = self.cmd_bot.get_command(sentence)
        print(f"명령어 리스트: {command_list}")

        # 명령어에 따른 응답 생성
        response = self.create_response(command_list)

        # 응답 메시지를 음성으로 출력 (TTS)
        response_message = self.tts_bot.speak(response)
        print(f"응답 메시지: {response_message}")
