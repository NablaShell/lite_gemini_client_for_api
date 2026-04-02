import os
import sqlite3
from datetime import datetime
from contextlib import contextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="Gemini 2.5 Flash Client", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini setup
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# Database setup
DB_PATH = os.getenv("DB_PATH", "chat_history.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                title TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT CHECK(role IN ('user', 'assistant')),
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)

# Models
class Message(BaseModel):
    text: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    error: Optional[str] = None

# API endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: Message):
    try:
        # Create or get conversation
        if message.conversation_id is None:
            with get_db() as conn:
                cursor = conn.execute(
                    "INSERT INTO conversations (title) VALUES (?)",
                    (message.text[:50] + "..." if len(message.text) > 50 else message.text,)
                )
                conversation_id = cursor.lastrowid
        else:
            conversation_id = message.conversation_id
        
        # Save user message
        with get_db() as conn:
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, 'user', message.text)
            )
        
        # Get Gemini response
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message.text,
        )
        
        # Save assistant response
        with get_db() as conn:
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, 'assistant', response.text)
            )
        
        return ChatResponse(response=response.text, conversation_id=conversation_id)
        
    except Exception as e:
        return ChatResponse(
            response="",
            conversation_id=message.conversation_id or 0,
            error=str(e)
        )

@app.get("/api/conversations")
async def get_conversations():
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT c.id, c.title, c.created_at, COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            GROUP BY c.id
            ORDER BY c.created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

@app.get("/api/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: int):
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (conversation_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int):
    with get_db() as conn:
        conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    return {"status": "deleted"}

@app.get("/api/health")
async def health():
    return {"status": "ok", "model": MODEL_NAME}

# Initialize DB and start
init_db()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
