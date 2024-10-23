import os
from dotenv import load_dotenv
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from google.oauth2 import service_account

from google.cloud import speech_v1p1beta1 as speech


class GoogleCloudSTT:
    def __init__(self):
        # .env 파일 로드
        load_dotenv()
        credentials_path = os.getenv("GOOGLE_SPEAK_CREDENTIALS")
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )

        # Speech-to-Text 클라이언트 초기화
        self.client = speech.SpeechClient(credentials=credentials)

    def __str__(self):
        return self.__class__.__name__

    def record(self, file_path, seconds):
        print(f"Recording {seconds} seconds of audio...")
        # 오디오 녹음 (마이크 테스트를 위해 sounddevice 사용)
        recording = sd.rec(
            int(seconds * 44100), samplerate=44100, channels=1, dtype=np.int16
        )
        sd.wait()  # 녹음이 끝날 때까지 대기

        # 녹음된 데이터를 wav 파일로 저장
        wavfile.write(file_path, 44100, recording)

        try:
            # Google Cloud Speech-to-Text API 호출을 위해 오디오 파일 읽기
            with open(file_path, "rb") as audio_file:
                content = audio_file.read()
                audio = speech.RecognitionAudio(content=content)

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=44100,
                language_code="ko-KR",
            )

            # Google Cloud Speech-to-Text API 호출
            response = self.client.recognize(config=config, audio=audio)
            text = (
                response.results[0].alternatives[0].transcript
                if response.results
                else ""
            )
            print(f"You said: {text}")
            return text

        except Exception as e:
            print(f"봇: 음성을 이해하지 못했습니다. {e}")
            return None
