import os
from datetime import datetime
from app.module.stt.google_stt_api import GoogleCloudSTT
from app.module.stt.speech_recognition_lib import SpeechRecognition


class STTBot:
    """
    음성 인식을 수행하는 STTBot 클래스입니다.
    음성 입력을 수행하고, 음성을 텍스트로 변환합니다.
    """

    def __init__(self, google_api=False):
        """
        STTBot 클래스 초기화. GoogleCloudSTT 모듈을 사용하여 음성 인식을 수행합니다.
        생성된 오디오 파일이 저장될 경로를 설정합니다.

        Args:
            google_api (bool): 구글 STT API를 사용할지 여부 (default: False)
        """
        if google_api:
            self.stt_module = GoogleCloudSTT()
        else:
            self.stt_module = SpeechRecognition()
        self.output_dir = "app/resource/audio/stt/"
        self.ensure_directory_exists(self.output_dir)

    def ensure_directory_exists(self, path: str):
        """
        경로가 존재하지 않으면 해당 경로를 생성합니다.

        Args:
            path (str): 생성할 경로
        """
        if not os.path.exists(path):
            os.makedirs(path)

    def create_file_path(self):
        """
        오디오 파일을 저장할 경로를 생성합니다.

        Returns:
            str: 오디오 파일 경로
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"{self.stt_module}_{timestamp}.wav")

    def listen(self, seconds=5):
        """
        지정된 시간 동안 음성 입력을 수행합니다.

        Args:
            seconds (int): 음성 입력을 수행할 시간 (default: 5)
        Returns:
            str: 음성 입력 결과
        """
        print(f"음성 입력을 시작합니다. {seconds}초간 마이크에 대고 말씀해주세요...")
        file_path = self.create_file_path()
        result = self.stt_module.record(file_path, seconds)
        return result

    def listen_unlimited(self):
        """
        무제한 음성 입력을 수행합니다.
        Returns:
            str: 음성 입력 결과
        """
        print("무제한 음성 입력을 시작합니다. 4초간 입력이 없으면 종료됩니다.")
        file_path = self.create_file_path()
        result = self.stt_module.record_unlimited(file_path)
        return result

    def listen_realtime(self):
        """
        실시간 음성 입력을 수행합니다.
        """
        print("실시간 음성 입력을 시작합니다. 종료하려면 Ctrl + C를 누르세요.")
        self.stt_module.record_and_recognize_realtime()
