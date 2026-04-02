import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="Gemini 2.5 Flash Client", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY не найден в .env файле")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

class Message(BaseModel):
    text: str

@app.post("/api/chat")
async def chat(message: Message):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message.text,
        )
        return {"response": response.text}
    except Exception as e:
        return {"response": "", "error": str(e)}

@app.get("/api/health")
async def health():
    return {"status": "ok", "model": MODEL_NAME}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Gemini {MODEL_NAME} готов на http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
