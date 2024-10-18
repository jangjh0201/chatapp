from gtts import gTTS


class gtts:
    def __init__(self, lang: str = "ko"):
        self.lang = lang

    def save_to_file(self, file_path, text: str):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(file_path)
        return file_path
