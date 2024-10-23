import os
from datetime import datetime
from playsound import playsound

from app.module.tts.google_tts_api import GoogleCloudTTS
from app.module.tts.gtts_lib import Gtts


class TTSBot:
    def __init__(self, google_api=False):
        if google_api:
            self.tts_module = GoogleCloudTTS()
        else:
            self.tts_module = Gtts()
        self.output_dir = "app/resource/audio/tts/"
        self.ensure_directory_exists(self.output_dir)

    def ensure_directory_exists(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    def create_file_path(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"{self.tts_module}_{timestamp}.mp3")

    def speak(self, text: str):
        file_path = self.create_file_path()
        self.tts_module.save_to_file(file_path, text)
        playsound(file_path)
        return text
