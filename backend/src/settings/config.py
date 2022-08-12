from pydantic import BaseSettings, Field
from fastapi_mail import ConnectionConfig
from redis import Redis


class Config(BaseSettings):
    class Config:
        env_file = ".env"

    mail_username: str = Field(env="MAIL_USERNAME")
    mail_password: str = Field(env="MAIL_PASSWORD")
    mail_from: str = Field(env="MAIL_FROM")
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"

    @property
    def mail_config(self):
        return ConnectionConfig(
            MAIL_USERNAME=self.mail_username,
            MAIL_PASSWORD=self.mail_password,
            MAIL_FROM=self.mail_from,
            MAIL_PORT=self.mail_port,
            MAIL_SERVER=self.mail_server,
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True,
            TEMPLATE_FOLDER="src/templates",
        )

    @property
    def setup_redis(self) -> Redis:
        return Redis(
            host="localhost",
            port=6379,
            db=0,
        )


config = Config()