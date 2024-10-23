from gtts import gTTS


class Gtts:
    def __init__(self, lang: str = "ko"):
        self.lang = lang

    def __str__(self):
        return self.__class__.__name__

    def save_to_file(self, file_path, text: str):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(file_path)
        return file_path
