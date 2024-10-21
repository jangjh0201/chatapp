import time
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import scipy.io.wavfile as wavfile


class SpeechRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 44100  # 샘플링 레이트 설정

    def __str__(self):
        return self.__class__.__name__

    def record(self, file_path, seconds):
        # 5초 동안 오디오 녹음 (마이크 테스트를 위해 sounddevice 사용)
        recording = sd.rec(
            int(seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.int16,
        )
        sd.wait()  # 녹음이 끝날 때까지 대기

        # 녹음된 데이터를 wav 파일로 저장 후, recognizer로 변환
        wavfile.write(file_path, 44100, recording)
        try:
            # 저장된 오디오 파일을 읽어서 음성 인식 수행
            with sr.AudioFile(file_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language="ko-KR")
                return text

        except sr.UnknownValueError as e:
            print(f"봇: 음성을 이해하지 못했습니다. {e}")
            return False
        except sr.RequestError as e:
            print(f"봇: 음성 인식 서비스에 접근할 수 없습니다: {e}")
            return False

    def record_unlimited(self, file_path):
        chunk_duration = 1  # 1초씩 녹음
        silence_duration = 4  # 4초간 무음일 경우 종료

        recorded_audio = []
        silence_start_time = None

        while True:
            # 1초 동안 녹음 진행
            chunk = sd.rec(
                int(chunk_duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.int16,
            )
            sd.wait()

            # 현재 녹음한 chunk를 추가
            recorded_audio.extend(chunk)

            # 음성의 소리 크기를 감지하여 무음인지 확인
            volume = np.linalg.norm(chunk) / len(chunk)

            if volume < 50:  # 임계값 50 이하일 경우 무음으로 간주
                if silence_start_time is None:
                    silence_start_time = time.time()
                elif time.time() - silence_start_time >= silence_duration:
                    print("4초간 무음이 발생했습니다. 녹음을 종료합니다.")
                    break
            else:
                silence_start_time = None  # 다시 소리가 나면 무음 시간 초기화

        # 녹음된 데이터를 wav 파일로 저장 후, recognizer로 변환
        wavfile.write(
            file_path,
            self.sample_rate,
            np.array(recorded_audio, dtype=np.int16),
        )

        try:
            # 저장된 오디오 파일을 읽어서 음성 인식 수행
            with sr.AudioFile(file_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language="ko-KR")
                return text

        except sr.UnknownValueError as e:
            print(f"봇: 음성을 이해하지 못했습니다. {e}")
            return False
        except sr.RequestError as e:
            print(f"봇: 음성 인식 서비스에 접근할 수 없습니다: {e}")
            return False

    def record_and_recognize_realtime(self):
        try:
            with sr.Microphone() as source:
                print(
                    "실시간 음성 입력을 시작합니다... 종료하려면 Ctrl + C를 누르세요."
                )
                self.recognizer.adjust_for_ambient_noise(
                    source
                )  # 주변 소음에 대해 조정

                while True:
                    print("말하세요...")
                    audio = self.recognizer.listen(source)  # 음성 입력 대기

                    try:
                        # Google Web Speech API를 사용하여 음성 인식
                        text = self.recognizer.recognize_google(audio, language="ko-KR")
                        print(f"인식된 문장: {text}")
                    except sr.UnknownValueError:
                        print(
                            "Google Web Speech API가 당신의 말을 이해하지 못했습니다."
                        )
                    except sr.RequestError as e:
                        print(
                            f"Google Web Speech API 서비스에 문제가 발생했습니다; {e}"
                        )
                        break

        except KeyboardInterrupt:
            print("\n실시간 음성 인식을 종료합니다.")
