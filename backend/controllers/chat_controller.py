import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import httpx
from bson import ObjectId
from fastapi import Depends, HTTPException, Request, status

from controllers.auth_controller import get_current_user
from models.chat import SendMessageRequest

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")


def generate_chat_response(messages: List[Dict[str, Any]]) -> str:
    if not LLM_API_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="LLM not configured")

    context = messages[-5:]
    prompt = [
        {"role": "system", "content": "You are a supportive conversational assistant for a victim distress monitoring prototype. Respond naturally, empathetically, and briefly. Do not diagnose or claim to be a doctor or psychologist. Focus on understanding the user's emotional state."},
    ]

    for item in context:
        prompt.append({"role": item["role"], "content": item["text"]})

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": LLM_MODEL,
        "messages": prompt,
        "temperature": 0.7,
    }

    response = httpx.post(f"{LLM_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def generate_distress_rank(messages: List[Dict[str, Any]]) -> int:
    if not LLM_API_KEY:
        return 1

    system_prompt = (
        "You are an AI-assisted distress assessment component for a victim-support prototype. "
        "Your task is NOT to diagnose a mental health condition. Analyze the provided conversation and estimate the user's current level of expressed psychological distress. "
        "Return an integer from 1 to 10. 1 means very low distress. 10 means extremely high distress. "
        "Consider only information explicitly expressed or reasonably evident from the conversation. "
        "Consider emotional distress, fear, anxiety, hopelessness, feeling unsafe, inability to cope, persistent negative emotions, worsening emotional state, threats or intimidation mentioned by the user, and other explicit indicators of distress. "
        "Do not diagnose, do not invent facts, do not infer sensitive attributes, and do not provide advice. "
        "Return ONLY valid JSON in exactly this format: {\"rank\": <integer>}"
    )

    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(messages, default=str)},
    ]

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": LLM_MODEL,
        "messages": prompt,
        "temperature": 0.2,
    }

    try:
        response = httpx.post(f"{LLM_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        parsed = json.loads(content)
        rank = int(parsed.get("rank", 1))
        if not 1 <= rank <= 10:
            raise ValueError("rank out of range")
        return rank
    except Exception:
        logging.exception("LLM rank generation failed; falling back to rank 1")
        return 1


def create_chat(request: Request, current_user: Dict[str, Any]) -> Dict[str, str]:
    db = request.app.state.db
    chat_document = {
        "user_id": str(current_user["_id"]),
        "messages": [],
        "is_closed": False,
        "rank_generated": False,
        "created_at": datetime.utcnow(),
        "closed_at": None,
    }
    result = db.chats.insert_one(chat_document)
    return {"chat_id": str(result.inserted_id)}


def send_message_to_chat(request: Request, current_user: Dict[str, Any], chat_id: str, payload: SendMessageRequest) -> Dict[str, Any]:
    db = request.app.state.db
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    chat = db.chats.find_one({"_id": ObjectId(chat_id)})
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    if str(chat["user_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if chat.get("is_closed"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chat is closed")

    user_message = {"role": "user", "text": payload.text, "timestamp": datetime.utcnow()}
    chat["messages"].append(user_message)
    db.chats.update_one({"_id": ObjectId(chat_id)}, {"$push": {"messages": user_message}})

    latest_messages = db.chats.find_one({"_id": ObjectId(chat_id)})["messages"][-5:]
    assistant_response = generate_chat_response(latest_messages)
    assistant_message = {"role": "assistant", "text": assistant_response, "timestamp": datetime.utcnow()}
    db.chats.update_one({"_id": ObjectId(chat_id)}, {"$push": {"messages": assistant_message}})

    return {"chat_id": chat_id, "message": assistant_message}


def get_chat(request: Request, current_user: Dict[str, Any], chat_id: str) -> Dict[str, Any]:
    db = request.app.state.db
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    chat = db.chats.find_one({"_id": ObjectId(chat_id)})
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    if str(chat["user_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    chat["chat_id"] = str(chat.pop("_id"))
    chat["user_id"] = str(chat["user_id"])
    return chat


def close_chat(request: Request, current_user: Dict[str, Any], chat_id: str) -> Dict[str, Any]:
    db = request.app.state.db
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    chat = db.chats.find_one({"_id": ObjectId(chat_id)})
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    if str(chat["user_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if chat.get("is_closed"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chat already closed")

    full_history = chat.get("messages", [])
    rank = generate_distress_rank(full_history)
    user = db.users.find_one({"_id": ObjectId(current_user["_id"])})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.users.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": {"rank": int(rank)}})
    db.chats.update_one(
        {"_id": ObjectId(chat_id)},
        {"$set": {"is_closed": True, "rank_generated": True, "closed_at": datetime.utcnow()}},
    )

    return {"message": "Chat closed successfully", "rank": int(rank)}
