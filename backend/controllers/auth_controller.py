import os
from datetime import datetime, timedelta
from typing import Any, Dict

import bcrypt
import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.user import UserLogin, UserRegister

JWT_SECRET = os.getenv("JWT_SECRET", "change-this-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
security = HTTPBearer()


def get_db(request: Request):
    return request.app.state.db


def register_user(request: Request, user_data: UserRegister) -> Dict[str, Any]:
    db = get_db(request)
    existing_user = db.users.find_one({"email": user_data.email.lower()})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    password_hash = bcrypt.hashpw(user_data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user_document = {
        "name": user_data.name.strip(),
        "email": user_data.email.lower(),
        "password_hash": password_hash,
        "rank": 1,
        "created_at": datetime.utcnow(),
    }
    result = db.users.insert_one(user_document)

    return {
        "user_id": str(result.inserted_id),
        "name": user_document["name"],
        "email": user_document["email"],
        "rank": user_document["rank"],
    }


def login_user(request: Request, login_data: UserLogin) -> Dict[str, str]:
    db = get_db(request)
    user = db.users.find_one({"email": login_data.email.lower()})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    stored_hash = user.get("password_hash", "")
    if not bcrypt.checkpw(login_data.password.encode("utf-8"), stored_hash.encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer"}


def create_access_token(user_id: str) -> str:
    expires_delta = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication token")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    db = get_db(request)
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
