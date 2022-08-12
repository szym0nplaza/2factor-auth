from typing import Any
from src.modules.login.ports import RedisPort
from src.modules.login.ports import UserDBPort, MailSenderPort
from src.modules.login.adapters import User


class MockMailSenderAdapter(MailSenderPort):
    def send_mail(self, **kwargs):
        return kwargs


class MockUserDBAdapter(UserDBPort):
    users: list = [User("test@mail.com", "zaq1@WSX")]

    def get_user(self, email: str):
        user = list(filter(lambda x: x.email == email, self.users))[-1]
        return user

    def insert_user(self, email: str, password: str):
        pass


class RedisMockAdapter(RedisPort):
    mock_cache_mem: dict = dict()

    def add(self, key, value) -> None:
        self.mock_cache_mem[key] = value

    def get(self, key) -> Any:
        return self.mock_cache_mem.get(key)

    def remove(self, key) -> None:
        self.mock_cache_mem.pop(key)
