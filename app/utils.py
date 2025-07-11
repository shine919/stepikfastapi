from datetime import datetime

from config import config, fake_db
from fastapi import Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(
    secret_key=config.secret_key,
    salt=config.salt,
)


async def check_token_time(user_id, time, response: Response):
    now = datetime.now().timestamp()
    if 180 < float(now) - float(time) < 300:
        token = await create_token(user_id)
        response.set_cookie(key="session_token", value=token, max_age=300, httponly=True)
        for user in fake_db:
            if user["user_id"] == user_id:
                user["session_token"] = token
        return True
    elif 180 > float(now) - float(time):
        return True
    else:
        response.delete_cookie(key="session_token")
        return False


async def create_token(user_id):
    timestamp = int(datetime.now().timestamp())
    data = f"{user_id}.{timestamp}"
    result = serializer.dumps(data)
    return f"{data}.{result}"


async def verify_token(token, response: Response, max_age=1800):
    token_list = token.split(".")
    signature = ".".join(token_list[2:])
    time = token_list[1]
    user_id = token_list[0]
    try:
        verify_signature = serializer.loads(signature, max_age=max_age)
        decoded_data = verify_signature.split(".")
        if decoded_data[0] == user_id and decoded_data[1] == time:
            pass
        else:
            raise BadSignature("msg")
        if not await check_token_time(user_id, time, response):
            raise SignatureExpired("msg")
        return {"message": "Success"}
    except BadSignature:
        return {"message": "Invalid session"}
    except SignatureExpired:
        return {"message": "Signature expired"}
