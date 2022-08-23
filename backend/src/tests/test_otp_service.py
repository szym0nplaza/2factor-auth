import pytest
import random
import ast
from modules.login.services import OTPService
from .helper_objects import RedisMockAdapter


class TestOTPService:
    email = "test@mail.com"
    redis = RedisMockAdapter()  # I declared it here to be able to mock number add
    service = OTPService(redis=redis)

    @pytest.fixture
    def load_mock_data(self) -> int:
        number = random.randint(10000, 99999)
        self.redis.add(f"{self.email}_otp", number)
        return number

    def test_otp_validation(self, load_mock_data):
        number = load_mock_data
        response = self.service.validate_otp(self.email, number)
        body = ast.literal_eval(response.body.decode("utf-8"))
        assert body.get("message") == "ok"
        assert response.status_code == 200

    def test_invalid_data(self, load_mock_data):
        response = self.service.validate_otp(self.email, 123)
        body = ast.literal_eval(response.body.decode("utf-8"))
        assert body.get("message") == "Incorrect code."
        assert response.status_code == 400
