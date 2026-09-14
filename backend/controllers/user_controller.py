from typing import Any, Dict

from fastapi import HTTPException, Request, status


def get_my_profile(request: Request, current_user: Dict[str, Any]) -> Dict[str, Any]:
    profile = {
        "user_id": str(current_user["_id"]),
        "name": current_user.get("name"),
        "email": current_user.get("email"),
        "rank": int(current_user.get("rank", 1)),
    }
    return profile
