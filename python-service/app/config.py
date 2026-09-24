import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_DATABASE = os.getenv("DB_DATABASE", "baotang360")
    DB_USERNAME = os.getenv("DB_USERNAME", "baotang_app")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "MatKhauManh123!")
    PY_SERVICE_TOKEN = os.getenv("PY_SERVICE_TOKEN", "")

    @property
    def dsn(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
            f"?charset=utf8mb4"
        )


config = Config()
