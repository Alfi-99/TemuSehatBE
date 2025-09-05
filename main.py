from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from google.adk.agents import Agent

# ======================================================
# 1. Define Fungsi Rules + Agent
# ======================================================
def rekomendasi_jamu(keluhan: str) -> dict:
    """Memberikan rekomendasi jamu atau obat herbal berdasarkan keluhan ringan.
       Jika indikasi red flag terdeteksi, sarankan segera ke dokter.
    """
    keluhan = keluhan.lower()

    # --- Red flag check ---
    red_flags = [
        "nyeri dada", "sakit jantung", "sesak napas", "pingsan",
        "muntah darah", "kelumpuhan", "sulit bicara", "kejang",
        "penglihatan hilang", "demam tinggi", "berdarah banyak",
    ]
    if any(flag in keluhan for flag in red_flags):
        return {
            "status": "red_flag",
            "message": "Segera konsultasi dokter. Ini tanda bahaya yang tidak bisa ditangani jamu."
        }

    # --- Keluhan ringan rules ---
    if "batuk" in keluhan and "dahak" in keluhan:
        return {
            "status": "success",
            "rekomendasi": "Jahe hangat + madu + jeruk nipis cocok untuk batuk berdahak."
        }
    elif "batuk" in keluhan and "kering" in keluhan:
        return {
            "status": "success",
            "rekomendasi": "Rebusan kunyit + madu atau daun sirih bagus untuk batuk kering."
        }
    elif "maag" in keluhan:
        return {
            "status": "success",
            "rekomendasi": "Air kunyit atau rebusan temulawak bisa membantu keluhan maag."
        }
    elif "pusing" in keluhan:
        return {
            "status": "success",
            "rekomendasi": "Wedang jahe atau teh daun pegagan bisa bantu meredakan pusing ringan."
        }
    elif "susah tidur" in keluhan:
        return {
            "status": "success",
            "rekomendasi": "Teh chamomile atau rebusan daun pandan dapat membantu tidur lebih nyenyak."
        }
    else:
        return {
            "status": "clarify",
            "clarify_message": (
                "Bisa ceritakan lebih detail tentang keluhanmu? Misalnya sifatnya "
                "(tajam, tumpul, berdenyut), gejala penyerta (demam, mual, dll), "
                "atau sudah berapa lama dirasakan."
            ),
        }

root_agent = Agent(
    name="jamu_rekomendasi_agent",
    model="gemini-2.0-flash",
    description="Agent yang menggali keluhan kesehatan sebelum memberikan rekomendasi jamu/herbal.",
    instruction=(
        "Kamu adalah konsultan herbal yang ramah dan semi-edukatif. "
        "Fokus pada penyakit ringan yang lazim ditangani jamu atau obat tradisional. "
        "Setiap kali user menyebutkan keluhan, jangan langsung kasih rekomendasi. "
        "Pertama, gali detail gejala: intensitas, lokasi, durasi, dan gejala penyerta. "
        "Jika indikasi penyakit berat atau tanda bahaya (red flag) terdeteksi, "
        "jangan berikan jamu apapun. Langsung sarankan ke dokter dan kembalikan "
        "{\"status\": \"red_flag\", \"message\": \"Segera konsultasi dokter\"} ke backend. "
        "Kalau gejalanya memang ringan, barulah beri rekomendasi jamu/herbal spesifik, "
        "lengkap dengan penjelasan singkat mengapa cocok."
    ),
    tools=[rekomendasi_jamu],
)

# ======================================================
# 2. FastAPI App + Endpoint
# ======================================================
app = FastAPI(title="TemuSehat Chatbot API")

# Simpan session sederhana
sessions: Dict[str, Dict[str, Any]] = {}

class SessionRequest(BaseModel):
    user_id: str
    session_id: str

class AskRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

@app.get("/")
def root():
    return {"status": "ok", "message": "TemuSehat API is running"}

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
@app.post("/ask")
def ask(req: AskRequest):
    if req.session_id not in sessions:
        return {"error": "Session not found"}

    # simpan pesan user ke history
    sessions[req.session_id]["history"].append({"role": "user", "content": req.message})

    # panggil agent
    response = root_agent.run(req.message)

    # simpan balasan ke history
    sessions[req.session_id]["history"].append({"role": "agent", "content": response})

    return {"reply": response, "session": sessions[req.session_id]}

# ----------------------------
@app.post("/end_session")
def end_session(req: SessionRequest):
    if req.session_id not in sessions:
        return {"error": "Session not found"}

    sessions[req.session_id]["state"]["status"] = "ended"
    return {"message": "Session ended", "session": sessions[req.session_id]}
