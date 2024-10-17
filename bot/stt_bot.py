import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from module.stt.google_stt_api import GoogleSpeechToText
from module.stt.speech_recognition_lib import SpeechRecognition


class STTBot:
    def __init__(self, google_api=False):
        if google_api:
            self.stt_manager = GoogleSpeechToText()
        else:
            self.stt_manager = SpeechRecognition()

    def listen(self, seconds=5):
        print(f"음성 입력을 시작합니다. {seconds}초간 마이크에 대고 말씀해주세요...")
        result = self.stt_manager.record(seconds)
        if result:
            print(f"인식된 문장: {result}")
            return result
        else:
            print("음성을 인식하지 못했습니다.")
            return False
