from .ports import MailSenderPort, UserDBPort, RedisPort
from starlette.responses import JSONResponse
from fastapi import BackgroundTasks
from src.settings.config import config
import random


class LoginService:
    def __init__(
        self, mailer: MailSenderPort, db: UserDBPort, redis: RedisPort
    ) -> None:
        self.mailer: MailSenderPort = mailer
        self.db: UserDBPort = db
        self.redis: RedisPort = redis
        self._add_mock_users()

    def _add_mock_users(self) -> None:
        self.db.insert_user(config.mail_from, "zaq1@WSX")
        self.db.insert_user("test2@mail.com", "123$%^QWE")

    def _generate_otp(self, email: str) -> int:
        code = random.randint(10000, 99999)
        self.redis.add(f"{email}_otp", code)
        return code

    def _send_mail(self, email: str, code: int, bg_tasks: BackgroundTasks) -> None:
        self.mailer.send_mail(
            subject="Your one time password",
            email_receivers=[email],
            body={"otp": code},
            background_tasks=bg_tasks,
        )

    def handle_login(self, data: dict, bg_tasks: BackgroundTasks) -> JSONResponse:
        user = self.db.get_user(data.get("email"))
        if not user or data.get("password") != user.password:
            return JSONResponse({"message": "Incorrect data."}, status_code=400)
        code = self._generate_otp(user.email)
        self._send_mail(user.email, code, bg_tasks)
        response = JSONResponse({"message": "ok"}, status_code=200)
        response.set_cookie(key="email", value=user.email)
        return response


class OTPService:
    def __init__(self, redis: RedisPort) -> None:
        self.redis: RedisPort = redis

    def validate_otp(self, email: str, given_code: int) -> JSONResponse:
        cached_code = self.redis.get(f"{email}_otp")
        if given_code == cached_code:
            self.redis.remove(f"{email}_otp")
            return JSONResponse({"message": "ok"}, status_code=200)
        return JSONResponse({"message": "Incorrect code."}, status_code=400)
