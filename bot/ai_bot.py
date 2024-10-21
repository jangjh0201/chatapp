from datetime import datetime
from functools import lru_cache
import os
from module.ai.google_vertex_api import GoogleCloudVertexAI


class AIBot:
    def __init__(self):
        """
        AIBot 클래스 초기화. GoogleCloudVertexAI 모듈을 사용하여 Vertex AI와 상호작용합니다.
        생성된 텍스트 파일이 저장될 경로와 역할 프롬프트 파일 경로를 설정합니다.
        """
        self.ai_module = GoogleCloudVertexAI(
            project_id="hifive-438811", location="asia-northeast3"
        )
        self.output_dir = "resource/script/ai/"
        self.role_prompt_file = (
            "resource/script/role.txt"  # 역할이 적힌 텍스트 파일 경로
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
        타임스탬프를 기반으로 고유한 파일 경로를 생성합니다.

        Returns:
            str: 생성된 파일 경로
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"{self.ai_module}_{timestamp}.txt")

    def load_role_prompt(self):
        """
        역할 프롬프트 파일에서 프롬프트를 읽어옵니다.

        Returns:
            str: 파일에서 읽어온 역할 프롬프트
        """
        if not os.path.exists(self.role_prompt_file):
            raise FileNotFoundError(f"File not found: {self.role_prompt_file}")

        with open(self.role_prompt_file, "r", encoding="utf-8") as file:
            role_prompt = file.read().strip()

        return role_prompt

    @lru_cache(maxsize=128)  # 최대 128개의 캐시 항목을 저장
    def generate_response(self, sentence: str):
        """
        사용자가 전달한 문장에 대해 AI 모델이 텍스트를 생성합니다.
        동일한 요청이 들어오면 캐시된 값을 반환합니다.
        """
        # 역할 프롬프트 파일에서 프롬프트를 읽어옴
        role_prompt = self.load_role_prompt()
        full_prompt = role_prompt + " " + sentence

        response = self.ai_module.generate_text("gemini-pro", full_prompt)

        # 실제 AI 모델 요청 코드를 여기 넣으세요
        return response
