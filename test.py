from google.cloud import speech_v1p1beta1 as speech
import speech_recognition as sr
from google.cloud import texttospeech_v1 as tts
import os
import playsound


# Google Cloud Speech-to-Text 클라이언트 설정
client = speech.SpeechClient()


def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for the trigger word '하이파이브'...")
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        audio_data = audio.get_wav_data()

        audio_content = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="ko-KR",
        )

        response = client.recognize(config=config, audio=audio_content)

        try:
            text = (
                response.results[0].alternatives[0].transcript
                if response.results
                else None
            )
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results, please check your internet connection.")
            return None


def get_gpt_response(user_input):
    role_description = (
        "당신은 음료를 만들어 주거나, 요청에 따라 서랍에 담겨져 있는 물건을 꺼내거나 다시 서랍에 넣어주는 로봇팔입니다. ",
        "다음은 당신이 수행할 수 있는 작업 목록입니다:",
        "- 음료 요청 받으면 만들기(분기 : 콤부차, 커피, 아이스티)",
        "- 현재 시간 요청 받으면 알려주기",
        "- 출근 준비 요청 받으면 물건들 꺼내주기",
        "- 알람 등록 요청받으면 등록했다고 대답하기",
        "각 요청을 수행하기 전에, 사용자가 요청한 것이 맞는지 다시 한 번 확인해 주세요.",
    )
    prompt = f"""{role_description} 
                사용자: {user_input} 
                로봇팔:"""
    # Gemini 모델 호출을 위한 로직을 여기에 추가
    response = "Gemini 모델의 응답을 여기에 처리"
    return response


def parse_command(gpt_response):
    # 간단한 명령어 파싱 로직 (예시)
    if "콤부차" in gpt_response:
        return "make_kombucha"
    elif "커피" in gpt_response:
        return "make_coffee"
    elif "아이스티" in gpt_response:
        return "make_icetea"
    elif "현재 시간" in gpt_response:
        return "tell_current_time"
    elif "출근 준비" in gpt_response:
        return "prepare_for_work"
    elif "알람 등록" in gpt_response:
        return "set_alarm"
    else:
        return None


def confirm_action(command):
    prompt = f"사용자가 '{command}' 요청에 대해 긍정적으로 응답했는지 부정적으로 응답했는지 확인해주세요."
    user_response = speak_text(f"'{command}' 요청을 하신 게 맞으신가요?")

    # Gemini 모델 호출 로직 추가
    gemini_prompt = f"""{prompt}
                    사용자: {user_response}
                    로봇팔:"""
    # 여기에 Gemini 모델 호출 코드를 추가하여 응답을 얻음
    # 예시로 response = Gemini 호출 결과

    response = "긍정"  # 실제로는 Gemini 모델 호출의 결과에 따라 긍정/부정을 반환함

    return response == "긍정"


def execute_command(command):
    if not confirm_action(command):
        speak_text("요청이 취소되었습니다.")
        return

    if command == "make_kombucha":
        speak_text("로봇팔이 콤부차를 만들고 있습니다.")
        # 실제 로봇팔 제어 로직을 여기에 추가
    elif command == "make_coffee":
        speak_text("로봇팔이 커피를 만들고 있습니다.")
        # 실제 로봇팔 제어 로직을 여기에 추가
    elif command == "make_icetea":
        speak_text("로봇팔이 아이스티를 만들고 있습니다.")
        # 실제 로봇팔 제어 로직을 여기에 추가
    elif command == "tell_current_time":
        from datetime import datetime

        current_time = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
        print(f"현재 시간은 {current_time} 입니다.")
        speak_text(f"현재 시간은 {current_time} 입니다.")
    elif command == "prepare_for_work":
        speak_text("로봇팔이 출근 준비를 위해 물건을 꺼내고 있습니다.")
        # 실제 로봇팔 제어 로직을 여기에 추가
    elif command == "set_alarm":
        speak_text("알람이 등록되었습니다.")
        speak_text("알람이 등록되었습니다.")
    else:
        speak_text("알 수 없는 명령입니다. 로봇팔을 제어할 수 없습니다.")


def speak_text(text):
    client = tts.TextToSpeechClient()
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=tts.SsmlVoiceGender.NEUTRAL
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open("response.mp3", "wb") as out:
        out.write(response.audio_content)
    playsound.playsound("response.mp3")
    os.remove("response.mp3")


# 챗봇 루프
if __name__ == "__main__":
    print("챗봇을 시작합니다. '종료'라고 말하면 종료됩니다.")
    while True:
        user_input = recognize_speech_from_mic()

        if user_input is None:
            continue

        # 트리거 단어 확인
        if "하이파이브" not in user_input:
            print(
                "Trigger word '하이파이브'가 감지되지 않았습니다. 다시 시도해 주세요."
            )
            continue

        if "종료" in user_input:
            print("챗봇을 종료합니다.")
            break

        # Gemini 모델로부터 응답 얻기
        gpt_response = get_gpt_response(user_input)
        print(f"Gemini 모델: {gpt_response}")

        # 명령 파싱 및 실행
        command = parse_command(gpt_response)
        if command:
            execute_command(command)

        # 응답을 음성으로 출력
        # 요청에 대한 확인 질문 후에만 실행하도록 수정됨
        speak_text(gpt_response)
