from fastapi import APIRouter, Request

from controllers.auth_controller import login_user, register_user
from models.user import UserLogin, UserRegister

router = APIRouter(tags=["auth"])


@router.post("/auth/register")
def register_user_route(request: Request, payload: UserRegister):
    return register_user(request, payload)


@router.post("/auth/login")
def login_user_route(request: Request, payload: UserLogin):
    return login_user(request, payload)
