from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from google.adk.agents import Agent

# ======================================================
# 1. Rules Function
# ======================================================
def rekomendasi_jamu(keluhan: str) -> dict:
    keluhan = keluhan.lower()

    # Red flag check
    red_flags = [
        "nyeri dada", "sakit jantung", "sesak napas", "pingsan",
        "muntah darah", "kelumpuhan", "sulit bicara", "kejang",
        "penglihatan hilang", "demam tinggi", "berdarah banyak",
    ]
    if any(flag in keluhan for flag in red_flags):
        return {
            "type": "red_flag",
            "message": "Segera konsultasi dokter. Ini tanda bahaya yang tidak bisa ditangani jamu."
        }

    # Keluhan ringan
    if "batuk" in keluhan and "dahak" in keluhan:
        return {"type": "rule", "rekomendasi": "Jahe hangat + madu + jeruk nipis cocok untuk batuk berdahak."}
    elif "batuk" in keluhan and "kering" in keluhan:
        return {"type": "rule", "rekomendasi": "Rebusan kunyit + madu atau daun sirih bagus untuk batuk kering."}
    elif "maag" in keluhan:
        return {"type": "rule", "rekomendasi": "Air kunyit atau rebusan temulawak bisa membantu keluhan maag."}
    elif "pusing" in keluhan:
        return {"type": "rule", "rekomendasi": "Wedang jahe atau teh daun pegagan bisa bantu meredakan pusing ringan."}
    elif "susah tidur" in keluhan:
        return {"type": "rule", "rekomendasi": "Teh chamomile atau rebusan daun pandan dapat membantu tidur lebih nyenyak."}
    else:
        return {"type": "clarify"}  # fallback ke LLM

# ======================================================
# 2. Initialize Agent
# ======================================================
root_agent = Agent(
    name="jamu_rekomendasi_agent",
    model="gemini-2.0-flash",
    description="Agent untuk menggali keluhan dan rekomendasi jamu/herbal.",
    instruction=(
        "Kamu adalah konsultan herbal yang ramah dan semi-edukatif. "
        "Gali detail gejala sebelum beri rekomendasi. "
        "Jika red flag, sarankan ke dokter. "
        "Kalau ringan, berikan rekomendasi jamu/herbal."
    ),
    tools=[rekomendasi_jamu],
)

# ======================================================
# 3. Wrapper yang kompatibel versi terbaru
# ======================================================
def agent_run(message: str) -> dict:
    try:
        # Cek rules dulu
        result = rekomendasi_jamu(message)

        if result.get("type") == "clarify":
            # Versi terbaru ADK
            plan = root_agent.plan(message)
            llm_response = plan.execute()
            return {"type": "llm", "reply": llm_response}

        return result
    except Exception as e:
        return {"type": "error", "message": str(e)}



# ======================================================
# 4. FastAPI App
# ======================================================
app = FastAPI(title="TemuSehat Chatbot API")

# Simpan session sederhana
sessions: Dict[str, Dict[str, Any]] = {}

# ----------------------------
# Request Models
# ----------------------------
class SessionRequest(BaseModel):
    user_id: str
    session_id: str

class AskRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

# ----------------------------
# Root
# ----------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "TemuSehat API is running"}

# ----------------------------
# Create Session
# ----------------------------
@app.post("/create_session")
def create_session(req: SessionRequest):
    sessions[req.session_id] = {
        "user_id": req.user_id,
        "state": {"status": "active"},
        "history": []
    }
    return {"message": "Session created", "session": sessions[req.session_id]}

# ----------------------------
# Ask Agent
# ----------------------------
@app.post("/ask")
def ask(req: AskRequest):
    if req.session_id not in sessions:
        return {"error": "Session not found"}

    # simpan pesan user
    sessions[req.session_id]["history"].append({"role": "user", "content": req.message})

    # panggil agent
    response = agent_run(req.message)

    # simpan balasan agent
    sessions[req.session_id]["history"].append({"role": "agent", "content": response})

    return {"reply": response, "session": sessions[req.session_id]}

# ----------------------------
# End Session
# ----------------------------
@app.post("/end_session")
def end_session(req: SessionRequest):
    if req.session_id not in sessions:
        return {"error": "Session not found"}

    sessions[req.session_id]["state"]["status"] = "ended"
    return {"message": "Session ended", "session": sessions[req.session_id]}
