from config import config, fake_db
from fastapi import FastAPI, HTTPException, Request, Response
from logger import logger
from models.models import UserLogin
from utils import create_token, verify_token

app = FastAPI()


if config.debug:
    app.debug = True
else:
    app.debug = False


@app.get("/")
async def root():
    logger.info(f"Connecting to database: {config.db.database_url}")
    return {"database_url": config.db.database_url}


@app.post("/login")
async def login_user(user: UserLogin, response: Response):
    for client in fake_db:
        if client["username"] == user.username and client["password"] == user.password:
            token = await create_token(client["user_id"])
            response.set_cookie(key="session_token", value=token, max_age=300, httponly=True)
            client["session_token"] = token
            return "congrats"
    return "User not found"


@app.get("/user")
async def get_user(request: Request, response: Response):
    session_token = request.cookies.get("session_token")
    if session_token:
        res = await verify_token(session_token, response)
        if res["message"] == "success":
            for client in fake_db:
                if client["session_token"] == session_token:
                    return client
            return "User with this cookie not Found"
        return HTTPException(status_code=401, detail=res["message"])
    return "You are not logged in"
