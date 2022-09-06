from pydantic import BaseModel


class LoginResponseSchema(BaseModel):
    message: str


class OTPRequestSchema(BaseModel):
    code: int


class OTPResponseSchema(BaseModel):
    message: str
    otp: bool