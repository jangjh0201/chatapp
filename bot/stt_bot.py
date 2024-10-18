from module.stt.google_stt_api import GoogleSpeechToText
from module.stt.speech_recognition_lib import SpeechRecognition


class STTBot:
    def __init__(self, google_api=False):
        if google_api:
            self.stt_module = GoogleSpeechToText("resource/audio/stt/temp_audio.wav")
        else:
            self.stt_module = SpeechRecognition("resource/audio/stt/temp_audio.wav")

    def listen(self, seconds=5):
        print(f"음성 입력을 시작합니다. {seconds}초간 마이크에 대고 말씀해주세요...")
        result = self.stt_module.record(seconds)
        if result:
            return result
        else:
            return False

    def listen_unlimited(self):
        print("무제한 음성 입력을 시작합니다. 4초간 입력이 없으면 종료됩니다.")
        result = self.stt_module.record_unlimited()
        if result:
            return result
        else:
            return False

    def listen_realtime(self):
        print("실시간 음성 입력을 시작합니다. 종료하려면 Ctrl + C를 누르세요.")
        self.stt_module.record_and_recognize_realtime()
