import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class AwsSetting(BaseSettings):
    check_expiration: bool = True
    jwt_header_prefix: str = "Bearer"
    jwt_header_name: str = "Authorization"
    endpoint_sagemaker: str = os.getenv("ENDPOINT_MODEL_SAGEMAKER")
    aws_credentials: dict = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }

    userpools: dict = {
        "sa": {
            "region": os.getenv("AWS_REGION"),
            "userpool_id": os.getenv("AWS_USER_POOL_ID"),
            "app_client_id": os.getenv("AWS_APP_CLIENT_ID"),
        }
    }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
