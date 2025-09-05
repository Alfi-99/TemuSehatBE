from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="TemuSehat Chatbot API")

# base URL ke agent utama (pastikan sesuai dengan port server agent-mu)
AGENT_BASE_URL = "http://localhost:8000"

# ==============================
# Request Models
# ==============================

class SessionRequest(BaseModel):
    user_id: str
    session_id: str


class AskRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


# ==============================
# 1. Create Session
# ==============================
@app.post("/create_session")
def create_session(req: SessionRequest):
    payload = {
        "state": {
            "status": "active"
        }
    }

    resp = requests.post(
        f"{AGENT_BASE_URL}/apps/multi_tool_agent/users/{req.user_id}/sessions/{req.session_id}",
        json=payload
    )

    try:
        return resp.json()
    except Exception:
        return {"error": resp.text}


# ==============================
# 2. Ask Agent (Chat)
# ==============================
@app.post("/ask")
def ask_agent(req: AskRequest):
    payload = {
        "app_name": "multi_tool_agent",
        "user_id": req.user_id,
        "session_id": req.session_id,
        "new_message": {
            "role": "user",
            "parts": [
                {"text": req.message}
            ]
        },
        "streaming": False
    }

    resp = requests.post(f"{AGENT_BASE_URL}/run_sse", json=payload)

    try:
        return resp.json()
    except Exception:
        return {"raw": resp.text}


# ==============================
# 3. End Session
# ==============================
@app.post("/end_session")
def end_session(req: SessionRequest):
    # biasanya bisa dihapus atau ditandai sebagai nonaktif
    payload = {
        "state": {
            "status": "ended"
        }
    }

    resp = requests.post(
        f"{AGENT_BASE_URL}/apps/multi_tool_agent/users/{req.user_id}/sessions/{req.session_id}",
        json=payload
    )

    try:
        return {"message": "Session ended", "response": resp.json()}
    except Exception:
        return {"message": "Session ended", "raw": resp.text}
