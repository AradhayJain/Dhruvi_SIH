from typing import Any, Dict

from fastapi import APIRouter, Depends, Request

from controllers.auth_controller import get_current_user
from controllers.chat_controller import close_chat, create_chat, get_chat, send_message_to_chat
from models.chat import SendMessageRequest

router = APIRouter(tags=["chat"])


@router.post("/chats")
def create_chat_route(request: Request, current_user: Dict[str, Any] = Depends(get_current_user)):
    return create_chat(request, current_user)


@router.post("/chats/{chat_id}/message")
def send_message_route(
    request: Request,
    chat_id: str,
    payload: SendMessageRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    return send_message_to_chat(request, current_user, chat_id, payload)


@router.get("/chats/{chat_id}")
def get_chat_route(
    request: Request,
    chat_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    return get_chat(request, current_user, chat_id)


@router.post("/chats/{chat_id}/close")
def close_chat_route(
    request: Request,
    chat_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    return close_chat(request, current_user, chat_id)
