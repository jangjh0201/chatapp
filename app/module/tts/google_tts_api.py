import os
from dotenv import load_dotenv
from google.oauth2 import service_account

from google.cloud import texttospeech


class GoogleCloudTTS:
    def __init__(self, lang: str = "ko"):
        """
        Google Cloud Text-to-Speech 클라이언트를 초기화합니다.

        Args:
            lang (str): 사용할 언어 (기본값: 'ko')
        """
        load_dotenv()
        credentials_path = os.getenv("GOOGLE_SPEAK_CREDENTIALS")
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )

        # Text-to-Speech 클라이언트 초기화
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)
        self.lang = lang

    def __str__(self):
        return self.__class__.__name__

    def save_to_file(self, file_path, text: str):
        # 요청 설정
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # 언어 설정
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.lang, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        # 오디오 설정 (MP3로 변환)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # TTS 요청
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # 결과 파일로 저장
        with open(file_path, "wb") as out:
            out.write(response.audio_content)

        return file_path
