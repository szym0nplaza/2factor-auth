from .ports import MailSenderPort, UserDBPort, RedisPort
from starlette.responses import JSONResponse
from fastapi import BackgroundTasks
from src.settings.config import config
import random


class LoginService:
    """Base login service for handling user authentication and generating OTP code"""

    def __init__(
        self, mailer: MailSenderPort, db: UserDBPort, redis: RedisPort
    ) -> None:
        self.mailer: MailSenderPort = mailer
        self.db: UserDBPort = db
        self.redis: RedisPort = redis
        self._add_mock_users()

    def _add_mock_users(self) -> None:
        # Add sample users for mock db
        self.db.insert_user(
            {"email": config.mail_from, "password": "zaq1@WSX", "otp": True}
        )
        self.db.insert_user(
            {"email": "test2@mail.com", "password": "123$%^QWE", "otp": False}
        )

    def _generate_otp(self, email: str) -> int:
        # Generate OTP code and save it in redis
        code = random.randint(10000, 99999) if config.send_mail else 11111
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

        # Check if user provided correct data
        if not user or data.get("password") != user.password:
            return JSONResponse({"message": "Incorrect data."}, status_code=400)
        code = self._generate_otp(user.email)

        # Check if user has OTP enabled and if config allows to send mail
        if user.otp and config.send_mail:
            self._send_mail(user.email, code, bg_tasks)
        response = JSONResponse({"message": "ok", "otp": user.otp}, status_code=200)

        # Set cookie to simulate maintaining user on the page
        response.set_cookie(key="email", value=user.email, domain="0.0.0.0")
        return response


class OTPService:
    """Class that provides methods for validating given otp code."""

    def __init__(self, redis: RedisPort) -> None:
        self.redis: RedisPort = redis

    def validate_otp(self, email: str, given_code: int) -> JSONResponse:
        cached_code = int(self.redis.get(f"{email}_otp"))
        # Validate OTP code with this from redis
        if given_code == cached_code:
            self.redis.remove(f"{email}_otp")
            return JSONResponse({"message": "ok"}, status_code=200)
        return JSONResponse({"message": "Incorrect code."}, status_code=400)
