import os
from datetime import datetime
from playsound import playsound
from module.tts.gtts_lib import gtts


class TTSBot:
    def __init__(self):
        self.tts_module = gtts()
        self.output_dir = "resource/audio/tts/"
        self.ensure_directory_exists(self.output_dir)

    def ensure_directory_exists(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    def speak(self, text: str):
        # 동적으로 파일명을 생성하여 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"gtts_output_{timestamp}.mp3")
        self.tts_module.save_to_file(output_file, text)
        playsound(output_file)
        return text
