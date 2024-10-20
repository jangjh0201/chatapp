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

    def create_file_path(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        module_name = self.tts_module.__class__.__name__
        return os.path.join(self.output_dir, f"{module_name}_{timestamp}.mp3")

    def speak(self, text: str):
        file_path = self.create_file_path()
        self.tts_module.save_to_file(file_path, text)
        playsound(file_path)
        return text
