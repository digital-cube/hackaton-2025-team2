# src/utils/jwt_handler.py
import os
import uuid
import jwt
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("JWT_SECRET", "change-me")  # set in env for production
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt(id_tenant, user_id, minutes: int, survey_completed: bool) -> str:
    # Normalize UUIDs to strings
    if isinstance(id_tenant, uuid.UUID):
        id_tenant = str(id_tenant)
    if isinstance(user_id, uuid.UUID):
        user_id = str(user_id)

    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,                 # user identifier
        "tenant": id_tenant,            # tenant identifier
        "survey_completed": survey_completed,  # survey status
        "iat": int(now.timestamp()),    # issued-at (numeric)
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),  # expiry (numeric)
        "iss": "carbonless",            # optional: issuer
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "user_id": payload.get("sub"),
            "id_tenant": payload.get("tenant"),
        }
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
