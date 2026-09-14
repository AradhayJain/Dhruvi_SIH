import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from routes.auth_routes import router as auth_router
from routes.chat_routes import router as chat_router
from routes.counsellor_routes import router as counsellor_router
from routes.user_routes import router as user_router


# Load .env
load_dotenv()


# Environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "victim_distress")


# Validate required environment variables
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set")


# FastAPI app
app = FastAPI(
    title="Victim Distress Monitoring MVP"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MongoDB
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
)

try:
    # Actually test the connection
    client.admin.command("ping")

    db = client[MONGO_DB_NAME]
    app.state.db = db

    # Create indexes
    db.users.create_index("email", unique=True)
    db.users.create_index("rank")
    db.chats.create_index("user_id")

    print("MongoDB connected successfully")

except Exception as e:
    print("MongoDB connection failed:")
    print(e)
    raise


# Routes
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(counsellor_router)


# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Run directly with: python main.py
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )