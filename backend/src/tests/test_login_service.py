import ast
from fastapi import BackgroundTasks
from modules.login.services import LoginService
from .helper_objects import MockMailSenderAdapter, MockUserDBAdapter, RedisMockAdapter


class TestLoginService:
    service = LoginService(
        db=MockUserDBAdapter(), mailer=MockMailSenderAdapter(), redis=RedisMockAdapter()
    )

    def test_login_handler(self):
        request_data = {"email": "test@mail.com", "password": "zaq1@WSX"}
        response = self.service.handle_login(request_data, BackgroundTasks())
        body = ast.literal_eval(response.body.decode("utf-8"))
        assert body.get("message") == "ok"
        assert response.status_code == 200

    def test_invalid_data(self):
        request_data = {"email": "test@mail.com", "password": "123"}
        response = self.service.handle_login(request_data, BackgroundTasks())
        body = ast.literal_eval(response.body.decode("utf-8"))
        assert body.get("message") == "Incorrect data."
        assert response.status_code == 400
