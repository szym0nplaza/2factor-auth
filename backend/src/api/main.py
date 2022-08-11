from typing import Optional
from fastapi import FastAPI, Request, Cookie
from src.modules.login.services import LoginService, OTPService
from src.modules.login.adapters import UserDBAdapter, MailSenderAdapter, RedisAdapter
import uvicorn


app = FastAPI()


@app.post("/login")
async def login(request: Request):
    service = LoginService(
        mailer=MailSenderAdapter(), db=UserDBAdapter(), redis=RedisAdapter()
    )
    data = await request.json()
    return service.handle_login(data)


@app.post("/validate-otp")
async def validate_otp(request: Request, email: Optional[str] = Cookie(None)):
    service = OTPService(redis=RedisAdapter())
    data = await request.json()
    return service.validate_otp(email, data.get("code"))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        log_level="debug",
        reload=True,
        port=8888,
    )
