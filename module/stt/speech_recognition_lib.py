import sounddevice as sd
import numpy as np
import speech_recognition as sr
import scipy.io.wavfile as wavfile


class SpeechRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def record(self, seconds):
        print(f"Recording {seconds} seconds of audio...")
        # 5초 동안 오디오 녹음 (마이크 테스트를 위해 sounddevice 사용)
        recording = sd.rec(
            int(seconds * 44100), samplerate=44100, channels=1, dtype=np.int16
        )
        sd.wait()  # 녹음이 끝날 때까지 대기

        # 녹음된 데이터를 wav 파일로 저장 후, recognizer로 변환
        wavfile.write("resource/audio/temp_audio.wav", 44100, recording)
        try:
            # 저장된 오디오 파일을 읽어서 음성 인식 수행
            with sr.AudioFile("resource/audio/temp_audio.wav") as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language="ko-KR")
                return text

        except sr.UnknownValueError as e:
            print(f"봇: 음성을 이해하지 못했습니다. {e}")
            return False
        except sr.RequestError as e:
            print(f"봇: 음성 인식 서비스에 접근할 수 없습니다: {e}")
            return False
