from bot import ai_bot, cmd_bot, stt_bot, tts_bot


class ChatApp:
    """
    음성 대화 시나리오를 수행하는 ChatApp 클래스.
    음성 입력을 받아들여 명령어를 추출하고, 해당 명령어에 따른 응답을 생성합니다.
    """

    def __init__(self):
        """
        ChatApp 클래스 초기화. STTBot, CMDBot, AIBot, TTSBot을 초기화합니다.
        생성된 봇들을 사용하여 음성 대화 시나리오를 수행합니다.
        """
        self.stt_bot = stt_bot.STTBot()
        self.cmd_bot = cmd_bot.CMDBot()
        self.ai_bot = ai_bot.AIBot()
        self.tts_bot = tts_bot.TTSBot(google_api=True)

    def run(self, mode="ai"):
        """
        ChatApp을 실행하는 메소드.
        음성 입력을 받아들여 명령어를 추출하고, 해당 명령어에 따른 응답을 생성합니다.
        Args:
            mode (str): 실행 모드 (default: "ai")
        """
        if mode == "normal":
            self.normal_mode()
        elif mode == "ai":
            self.ai_mode()

    def normal_mode(self):
        """
        일반 모드로 ChatApp을 실행하는 메소드.
        음성 입력을 받아들여 명령어를 추출하고, 해당 명령어에 따른 응답을 생성합니다.
        """
        # 음성 입력받기 (STT)
        sentence = self.stt_bot.listen()
        print(f"음성 입력: {sentence}")

        # 명령어 추출 (CMD)
        command_list = self.cmd_bot.get_command(sentence)
        print(f"명령어 리스트: {command_list}")

        # 명령어에 따른 응답 생성
        response = self.cmd_bot.create_response(command_list)

        # 응답 메시지를 음성으로 출력 (TTS)
        self.tts_bot.speak(response)
        print(f"봇: {response}")

    def ai_mode(self):
        """
        AI 모드로 ChatApp을 실행하는 메소드.
        음성 입력을 받아들여 AI 모델을 사용하여 응답을 생성합니다.
        """
        # 음성 입력받기 (STT)
        sentence = self.stt_bot.listen()
        print(f"음성 입력: {sentence}")

        # AI 모델을 사용하여 응답 생성
        response = self.ai_bot.generate_response(sentence)

        # 응답 파싱
        parsed_response, parsed_commands = cmd_bot.CMDBot().parse_sentence(response)

        # 응답 메시지를 음성으로 출력 (TTS)
        self.tts_bot.speak(parsed_response)
        print(f"봇: {parsed_response}")
        if parsed_commands:
            print(f"{parsed_commands}")
