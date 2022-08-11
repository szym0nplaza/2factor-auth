from src.settings.config import config, setup_redis
from fastapi_mail import FastMail, MessageSchema
from fastapi import BackgroundTasks
from dataclasses import dataclass
from typing import Dict, Union
from .ports import MailSenderPort, UserDBPort, RedisPort


@dataclass
class User:
    email: str
    password: str


class UserDBAdapter(UserDBPort):
    """Helper class for mock users"""
    users: Dict[str, User] = dict()

    def get_user(self, email: str) -> Union[User, None]:
        return self.users.get(email)

    def insert_user(self, email: str, password: str) -> None:
        self.users[email] = User(email=email, password=password)


class MailSenderAdapter(MailSenderPort):
    """
    Base email sender class
    """

    def send_mail(
        self,
        subject: str,
        email_receivers: list,
        body: dict,
        background_tasks: BackgroundTasks,
    ) -> None:
        message = MessageSchema(
            subject=subject,
            recipients=email_receivers,
            template_body=body,
            subtype="html",
        )

        fm = FastMail(config.mail_config)
        background_tasks.add_task(
            fm.send_message, message=message, template_name="mail-template.html"
        )

class RedisAdapter(RedisPort):
    def __init__(self, redis = setup_redis()):
        self.redis = redis

    def add(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        value = self.redis.get(key)
        if value:
            return value.decode("utf-8")

    def remove(self, key):
        self.redis.delete(key)