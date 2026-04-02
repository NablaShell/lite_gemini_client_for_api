# Gemini 3.1 Flash Lite Local Client

A lightweight, self-hosted client for Google's Gemini 3.1 Flash Lite API. No heavy JS dependencies, full chat history, and Docker-ready.

## Why this instead of web version?

Because `gemini.google.com`:
- 🐌 Loads **megabytes of JavaScript** and heavy dependencies
- 📡 Wastes bandwidth even for simple chats
- 🎨 Locked into Google's design with zero customization

**This client:**
- ⚡ **Lightweight** — minimal code, no bloat
- 🔓 **Open Source** — full control over everything
- 🎨 **Fully customizable** — change themes, behavior, features
- 🐳 **Docker ready** — runs the same on any system
- 💾 **Chat history** — SQLite database with conversation management
- 💨 **Fast** — instant responses, no lag

## Quick Start

### 1. Get an API Key
- Go to https://aistudio.google.com/app/apikey
- Click "Create API Key"
- Copy your key

### 2. Configure the key
Create a `.env` file:
```env
GEMINI_API_KEY=your_key_here
```
3. Run with Docker (recommended)
```bash

# Build and start
docker compose up -d
```
# Open in browser
http://localhost:8000

Or run without Docker (for development)
```bash

# Install dependencies
pip install -r requirements.txt

# Run server
python backend.py
```

Features

    🤖 Gemini 3.1 Flash Lite — 500 RPD, 250K token context

    💬 Chat history — all conversations saved in SQLite

    📁 Conversation management — create, switch, delete dialogs

    🎨 Markdown support — code blocks, bold, italic

    🐳 Docker & volume — persistent storage

    🌙 Dark theme — easy on the eyes

    ⚡ Fast & lightweight — no framework bloat

Docker Commands
```bash

# Start container
docker compose up -d

# Stop container
docker compose down

# View logs
docker compose logs -f

# Restart
docker compose restart

# Complete cleanup (with volumes)
docker compose down -v

# Rebuild image
docker compose build --no-cache
```

API Endpoints
Method	Endpoint	Description
POST	/api/chat	Send message to Gemini
GET	/api/conversations	List all conversations
GET	/api/conversations/{id}/messages	Get messages from conversation
DELETE	/api/conversations/{id}	Delete conversation
GET	/api/health	Health check

Example API call
```bash

curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, Gemini!"}'
```
Troubleshooting
Problem	Solution
404 error	Check model name in backend.py (should be gemini-3.1-flash-lite)
No response / API error	Check API key in .env file
Port 8000 already in use	Change port in docker-compose.yml and backend.py
Docker not found	Install Docker: https://docs.docker.com/get-docker/
Permission denied on /data	Run mkdir -p data && chmod 755 data
Container name conflict	Run docker rm -f gemini-flash-client then docker compose up -d
Project Structure
```text

gemini-client/
├── backend.py          # FastAPI server with Gemini integration
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Container orchestration
├── .env               # API key (your secret, not in repo)
├── .dockerignore      # Files excluded from Docker
├── run.sh / run.bat   # Quick start scripts
└── static/            # Frontend files
    ├── index.html     # Main page with chat UI
    └── style.css      # Dark theme styles
```
Customization

Want to change the look or add features?

    CSS styles — edit static/style.css

    Chat behavior — edit static/script.js

    Backend logic — edit backend.py

    Add search — extend SQLite queries

    Export chats — add JSON/Markdown export

    Voice input — add Web Speech API

No limits — it's your local client! 🔧
Tech Stack

    Backend: Python 3.12 + FastAPI + google-genai SDK

    Frontend: Pure HTML/CSS/JS (no frameworks!)

    Database: SQLite (embedded, no extra services)

    Container: Docker + Docker Compose

    Model: Gemini 3.1 Flash Lite (500 RPM, 250K context)

License

MIT — do whatever you want, copy, modify, sell, embed anywhere.
Credits

    Google for Gemini API

    You for using and improving 🤝

🎉 Ready! You now have your own fast, lightweight, and fully controllable Gemini client.
