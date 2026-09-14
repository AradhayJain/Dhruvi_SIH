from typing import Any, Dict

from fastapi import APIRouter, Request

from controllers.counsellor_controller import (
    get_counsellor_user_chats,
    get_counsellor_user_detail,
    get_counsellor_users,
)

router = APIRouter(tags=["counsellor"])


@router.get("/counsellor/users")
def get_counsellor_users_route(request: Request):
    return get_counsellor_users(request)


@router.get("/counsellor/users/{user_id}")
def get_counsellor_user_detail_route(request: Request, user_id: str):
    return get_counsellor_user_detail(request, user_id)


@router.get("/counsellor/users/{user_id}/chats")
def get_counsellor_user_chats_route(request: Request, user_id: str):
    return get_counsellor_user_chats(request, user_id)
