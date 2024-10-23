from datetime import datetime
import os
from app.module.ai.google_vertex_api import GoogleCloudVertexAI


class AIBot:
    def __init__(self):
        """
        AIBot 클래스 초기화. GoogleCloudVertexAI 모듈을 사용하여 Vertex AI와 상호작용합니다.
        생성된 텍스트 파일이 저장될 경로와 역할 프롬프트 파일 경로를 설정합니다.
        """
        self.output_dir = "app/resource/script/ai/"
        self.scenario_path = (
            self.create_file_path()
        )  # 초기화 시 새 시나리오 파일 경로 생성
        self.role_prompt_path = (
            "app/resource/script/prompt/vertex_role.txt"  # 역할이 적힌 텍스트 파일 경로
        )
        self.ai_module = GoogleCloudVertexAI(
            project_id="hifive-438811",
            location="asia-northeast3",
            model_name="gemini-1.5-flash-001",
            role_prompt=self.load_role_prompt(),
        )

    def ensure_directory_exists(self, path: str):
        """
        경로가 존재하지 않으면 해당 경로를 생성합니다.

        Args:
            path (str): 생성할 경로
        """
        if not os.path.exists(path):
            os.makedirs(path)

    def create_file_path(self):
        """
        타임스탬프를 기반으로 고유한 시나리오 파일 경로를 생성합니다.

        Returns:
            str: 생성된 시나리오 파일 경로
        """
        self.ensure_directory_exists(self.output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"scenario_{timestamp}.txt")

    def load_role_prompt(self):
        """
        역할 프롬프트 파일에서 프롬프트를 읽어옵니다.

        Returns:
            str: 파일에서 읽어온 역할 프롬프트
        """
        if not os.path.exists(self.role_prompt_path):
            raise FileNotFoundError(f"File not found: {self.role_prompt_path}")

        with open(self.role_prompt_path, "r", encoding="utf-8") as file:
            role_prompt = file.read().strip()

        return role_prompt

    def append_to_scenario(self, text: str):
        """
        시나리오 파일에 텍스트를 추가합니다.

        Args:
            text (str): 추가할 텍스트
        """
        with open(self.scenario_path, "a", encoding="utf-8") as file:
            file.write(f"{text}\n")

    def generate_response(self, sentence: str):
        """
        대화 기록과 사용자가 전달한 문장을 결합하여 AI 모델에 전달하고, AI의 응답을 반환합니다.
        """

        # 사용자가 입력한 문장을 시나리오 파일에 추가
        self.append_to_scenario(f"User: {sentence}")

        # role prompt와 사용자 문장을 결합하여 AI에게 전달
        role_prompt = self.load_role_prompt()
        full_prompt = f"{role_prompt}\nUser: {sentence}"

        # AI 모델을 사용하여 응답 생성
        response = self.ai_module.generate_text(full_prompt)

        # AI의 응답을 시나리오 파일에 추가
        self.append_to_scenario(f"AI: {response}")

        return response
