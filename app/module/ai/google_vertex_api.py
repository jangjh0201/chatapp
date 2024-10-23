import os
from dotenv import load_dotenv
from google.oauth2 import service_account

import vertexai
from vertexai.preview.generative_models import GenerativeModel


class GoogleCloudVertexAI:
    def __init__(
        self, project_id: str, location: str, model_name: str, role_prompt: str
    ):
        """
        Vertex AI Client를 초기화합니다.

        Args:
            project_id (str): Google Cloud 프로젝트 ID
            location (str): Vertex AI 리전
        """
        load_dotenv()
        credentials_path = os.getenv("GOOGLE_VERTEX_CREDENTIALS")
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )

        # Vertex AI 초기화
        vertexai.init(project=project_id, location=location, credentials=credentials)
        self.model = GenerativeModel(model_name=model_name)
        self.model.generate_content(role_prompt)

    def __str__(self):
        return self.__class__.__name__

    def generate_text(self, user_message: str) -> str:
        """
        주어진 사용자 메시지에 대해 Generative Model을 사용하여 텍스트를 생성합니다.

        Args:
            model_name (str): 사용할 모델의 이름 (예: 'gemini-pro')
            user_message (str): 생성할 텍스트의 입력 메시지

        Returns:
            str: 생성된 텍스트
        """
        response = self.model.generate_content(user_message)
        return response.text
