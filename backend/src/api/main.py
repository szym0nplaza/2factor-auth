from typing import Optional
from fastapi import FastAPI, Request, Cookie, BackgroundTasks
from src.modules.login.services import LoginService, OTPService
from src.modules.login.adapters import UserDBAdapter, MailSenderAdapter, RedisAdapter
import uvicorn


app = FastAPI()


@app.post("/api/login")
async def login(request: Request, bg_tasks: BackgroundTasks):
    service = LoginService(
        mailer=MailSenderAdapter(), db=UserDBAdapter(), redis=RedisAdapter()
    )
    data = await request.json()
    return service.handle_login(data, bg_tasks)


@app.post("/api/validate-otp")
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
