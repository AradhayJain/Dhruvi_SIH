from typing import Any, Dict, List

from bson import ObjectId
from fastapi import HTTPException, Request, status


def get_counsellor_users(request: Request) -> Dict[str, List[Dict[str, Any]]]:
    db = request.app.state.db
    users = list(
        db.users.find({}, {"password_hash": 0}).sort([("rank", -1), ("created_at", -1)])
    )

    result = []
    for user in users:
        result.append(
            {
                "user_id": str(user["_id"]),
                "name": user.get("name"),
                "rank": int(user.get("rank", 1)),
            }
        )

    return {"users": result}


def get_counsellor_user_detail(request: Request, user_id: str) -> Dict[str, Any]:
    db = request.app.state.db
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = db.users.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "user_id": str(user["_id"]),
        "name": user.get("name"),
        "rank": int(user.get("rank", 1)),
    }


def get_counsellor_user_chats(request: Request, user_id: str) -> Dict[str, List[Dict[str, Any]]]:
    db = request.app.state.db
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = db.users.find_one({"_id": ObjectId(user_id)}, {"_id": 1})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    chats = list(db.chats.find({"user_id": user_id}).sort("created_at", -1))
    result = []

    for chat in chats:
        result.append(
            {
                "chat_id": str(chat["_id"]),
                "is_closed": bool(chat.get("is_closed", False)),
                "rank_generated": bool(chat.get("rank_generated", False)),
                "created_at": chat.get("created_at"),
                "closed_at": chat.get("closed_at"),
                "message_count": len(chat.get("messages", [])),
            }
        )

    return {"chats": result}
