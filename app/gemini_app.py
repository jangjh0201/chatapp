import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.bot import stt_bot, tts_bot
from app.utils.cleaner import cleanup_folders
from backend.task_manager import TaskManager  # TaskManager 임포트


class GeminiApp:
    """
    Google Cloud Gemini API와 음성 기반 대화 시나리오를 수행하는 GeminiApp 클래스.
    STT, TTS 봇을 사용하여 음성 명령을 인식하고 처리합니다.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        GeminiApp 초기화 및 STT/TTS 봇 설정.

        Args:
            model_name (str): 사용할 모델의 이름 (default: 'gemini-1.5-flash')
        """
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # STT와 TTS 봇 초기화
        self.stt_bot = stt_bot.STTBot()
        self.tts_bot = tts_bot.TTSBot(google_api=True)

        # 트리거 단어 설정
        self.trigger_word = "하이파이브"

        # Google Gemini API 모델 설정
        self.system_instruction = self.load_role_prompt(
            "app/resource/script/prompt/gemini_role.txt"
        )
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=self.system_instruction,
            generation_config={"response_mime_type": "application/json"},
        )
        self.chat_session = self.model.start_chat(history=[])

        # 특정 폴더의 파일 삭제
        cleanup_folders(["app/resource/audio/stt", "app/resource/audio/tts"])

        # TaskManager 초기화
        self.task_manager = TaskManager()

    def load_role_prompt(self, file_path: str) -> str:
        """
        역할 프롬프트 파일에서 내용을 읽어옵니다.

        Args:
            file_path (str): 파일 경로

        Returns:
            str: 파일에서 읽어온 역할 프롬프트
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    def run(self):
        """
        실시간 음성 명령어 청취 및 트리거 단어 인식 후 대화 수행.
        """
        print(
            f"청취 모드를 시작합니다. '{self.trigger_word}'라고 말하면 대화가 시작됩니다."
        )

        while True:
            # 트리거 단어가 나올 때까지 계속 청취
            sentence = self.stt_bot.listen()
            print(f"청취 중: {sentence}")

            if self.trigger_word in sentence:
                # 트리거 단어 감지 시 응답
                self.tts_bot.speak("네, 무엇을 도와드릴까요?")
                print("봇: 네, 무엇을 도와드릴까요?")
                # 명령어 대화 모드로 전환
                self.conversation_mode()

    def conversation_mode(self):
        """
        트리거 이후 대화를 수행하는 메소드.
        명령어가 있으면 대화를 종료합니다.
        """
        while True:
            sentence = self.stt_bot.listen()  # 대화 중 음성 입력
            print(f"음성 입력: {sentence}")

            # AI 모델을 사용하여 응답 생성
            response = self.chat_session.send_message(sentence)
            response_data = json.loads(response.text)  # JSON 형식의 응답을 받음
            answer = response_data.get("answer", "")
            commands = response_data.get("commands", [])

            # answer는 TTS로 출력
            self.tts_bot.speak(answer)
            print(f"봇: {answer}")

            # 명령어 처리
            if commands:
                print(f"{commands}")
                break  # 명령어가 있으면 대화 종료

        print("청취 모드로 돌아갑니다.\n")

    def handle_commands(self, commands):
        """
        단일 명령어 리스트를 처리하고 해당 작업을 수행합니다.
        """
        # commands 리스트에서 명사(action)와 동사(task)를 분리
        action, task = commands[0], commands[1]
        print(f"Action: {action}, Task: {task}")

        if self.task_manager.can_use_robot():
            if action in ["커피", "차", "아이스티"] and task == "만들기":
                # 음료 만들기 작업을 비동기로 처리
                self.task_manager.start_making_drink()

            elif action == "물건들" and task in ["꺼내기", "정리하기"]:
                # 서랍 빼기 또는 정리가 가능하면 작업을 시작
                if task == "꺼내기":
                    self.task_manager.start_emptying_drawer()
                else:
                    self.task_manager.start_storing_drawer()

            elif action == "대화" and task == "끝내기":
                self.tts_bot.speak("대화를 종료합니다.")

        else:
            self.tts_bot.speak("이미 작업 중입니다.")
            print("이미 작업 중입니다.")

    def __str__(self):
        return self.__class__.__name__
