from typing import Optional
from fastapi import FastAPI, Cookie, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.modules.login.schemas import (
    LoginResponseSchema,
    OTPResponseSchema,
    OTPRequestSchema,
)
from src.modules.login.services import LoginService, OTPService
from src.modules.login.adapters import (
    UserDBAdapter,
    MailSenderAdapter,
    RedisAdapter,
    User,
)
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/api/login",
    responses={
        "200": {"model": LoginResponseSchema},
        "400": {"model": LoginResponseSchema},
    },
)
async def login(user: User, bg_tasks: BackgroundTasks):
    # Use dependency injection for proper application work
    service = LoginService(
        mailer=MailSenderAdapter(), db=UserDBAdapter(), redis=RedisAdapter()
    )
    return service.handle_login(user.__dict__, bg_tasks)


@app.post("/api/validate-otp", responses={
        "200": {"model": OTPResponseSchema},
        "400": {"model": OTPResponseSchema},
    },)
async def validate_otp(code: OTPRequestSchema, email: Optional[str] = Cookie(None)):
    service = OTPService(redis=RedisAdapter())
    return service.validate_otp(email, code.code)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        log_level="debug",
        reload=True,
        port=8888,
    )
