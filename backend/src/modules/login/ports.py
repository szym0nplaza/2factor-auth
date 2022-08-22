from abc import ABC, abstractmethod
from fastapi import BackgroundTasks


class MailSenderPort(ABC):
    @abstractmethod
    def send_mail(
        self,
        subject: str,
        email_receivers: list,
        body: dict,
        background_tasks: BackgroundTasks,
    ):
        raise NotImplementedError


class UserDBPort(ABC):
    users: dict

    def get_user(self, email: str):
        raise NotImplementedError

    def insert_user(self, data: dict):
        raise NotImplementedError


class RedisPort(ABC):

    @abstractmethod
    def add(self, key, value):
        return NotImplementedError
    
    @abstractmethod
    def get(self, key):
        return NotImplementedError
    
    @abstractmethod
    def remove(self, key):
        return NotImplementedError