from app.chatapp import ChatApp
from app.gemini_app import GeminiApp

if __name__ == "__main__":
    # ChatApp 인스턴스 생성 및 실행
    app = ChatApp()
    gemini_app = GeminiApp()

    # 앱을 계속 실행 (while 루프로 지속)
    while True:
        # app.run()
        gemini_app.run()
        print("앱을 계속 실행 중입니다. 종료하려면 Ctrl + C를 누르세요.")
