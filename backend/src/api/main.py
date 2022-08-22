from typing import Optional
from fastapi import FastAPI, Request, Cookie, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.modules.login.services import LoginService, OTPService
from src.modules.login.adapters import UserDBAdapter, MailSenderAdapter, RedisAdapter, User
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/login")
async def login(user: User, bg_tasks: BackgroundTasks):
    service = LoginService(
        mailer=MailSenderAdapter(), db=UserDBAdapter(), redis=RedisAdapter()
    )
    return service.handle_login(user.__dict__, bg_tasks)


@app.post("/api/validate-otp")
async def validate_otp(request: Request, email: Optional[str] = Cookie(None)):
    print(email)
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
