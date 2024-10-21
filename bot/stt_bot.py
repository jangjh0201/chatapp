from datetime import datetime
import os
from module.stt.google_stt_api import GoogleCloudSTT
from module.stt.speech_recognition_lib import SpeechRecognition


class STTBot:
    def __init__(self, google_api=False):
        if google_api:
            self.stt_module = GoogleCloudSTT()
        else:
            self.stt_module = SpeechRecognition()
        self.output_dir = "resource/audio/stt/"
        self.ensure_directory_exists(self.output_dir)

    def ensure_directory_exists(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    def create_file_path(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"{self.stt_module}_{timestamp}.wav")

    def listen(self, seconds=5):
        print(f"음성 입력을 시작합니다. {seconds}초간 마이크에 대고 말씀해주세요...")
        file_path = self.create_file_path()
        result = self.stt_module.record(file_path, seconds)
        if result:
            return result
        else:
            return False

    def listen_unlimited(self):
        print("무제한 음성 입력을 시작합니다. 4초간 입력이 없으면 종료됩니다.")
        file_path = self.create_file_path()
        result = self.stt_module.record_unlimited(file_path)
        if result:
            return result
        else:
            return False

    def listen_realtime(self):
        print("실시간 음성 입력을 시작합니다. 종료하려면 Ctrl + C를 누르세요.")
        self.stt_module.record_and_recognize_realtime()
