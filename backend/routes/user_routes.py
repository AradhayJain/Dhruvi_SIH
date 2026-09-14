from typing import Any, Dict

from fastapi import APIRouter, Depends, Request

from controllers.auth_controller import get_current_user
from controllers.user_controller import get_my_profile

router = APIRouter(tags=["user"])


@router.get("/users/me")
def read_my_profile(request: Request, current_user: Dict[str, Any] = Depends(get_current_user)):
    return get_my_profile(request, current_user)
