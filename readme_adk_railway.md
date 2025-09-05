# TemuSehat Agent (ADK) – Railway Deployment Guide

## Deskripsi
Ini adalah panduan untuk menjalankan agent **`jamu_rekomendasi_agent`** menggunakan **ADK API Server** yang sudah dideploy di **Railway**. Panduan ini mencakup: setup, start session, kirim pesan, dan end session.

---

## 1️⃣ Setup Environment

1. Clone repo project ke lokal:
```bash
git clone <repo-url>
cd TemuSehatBE
```

2. Aktifkan virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Buat file `.env` (jika belum ada):
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=<API_KEY_ANDA>
```

---

## 2️⃣ Railway Deployment

1. **Custom Start Command** (Railway Settings → Deploy → Start Command):
```bash
adk api_server
```
> Ini akan langsung menjalankan **ADK API Server** di Railway tanpa perlu `main.py`.

2. Deploy ke Railway.  
3. Pastikan log muncul:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 3️⃣ API Endpoints

Railway URL: `https://temusehatbe-production.up.railway.app`

| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/apps/{app_name}/users/{user_id}/sessions/{session_id}` | POST | Buat / start session |
| `/run` | POST | Kirim pesan ke agent (ask) |
| `/apps/{app_name}/users/{user_id}/sessions/{session_id}` | DELETE | Hapus / end session |

---

## 4️⃣ PowerShell cURL Commands

### 4.1 Buat Session
```powershell
curl -X POST https://temusehatbe-production.up.railway.app/apps/jamu_rekomendasi_agent/users/u_123/sessions/s_123 -H "Content-Type: application/json" -d "{\"state\":{}}"
```

### 4.2 Kirim Pesan / Ask Agent
```powershell
curl -X POST https://temusehatbe-production.up.railway.app/run -H "Content-Type: application/json" -d "{\"app_name\":\"jamu_rekomendasi_agent\",\"user_id\":\"u_123\",\"session_id\":\"s_123\",\"new_message\":{\"role\":\"user\",\"parts\":[{\"text\":\"Halo\"}]}}"
```

### 4.3 Hapus / End Session
```powershell
curl -X DELETE https://temusehatbe-production.up.railway.app/apps/jamu_rekomendasi_agent/users/u_123/sessions/s_123
```

> ⚠ Catatan:
> - Jangan pakai backtick di tengah JSON di PowerShell.  
> - Gunakan escape `\"` untuk double quote dalam JSON.  
> - Urutan: **start session → ask → end session**.

---

## 5️⃣ Testing / Debugging

1. Setelah server jalan, buka **Swagger UI**:
```
https://temusehatbe-production.up.railway.app/docs
```

2. Bisa langsung test endpoint dari browser.

---

## 6️⃣ Tips

- Jika muncul `Session already exists`, hapus session dulu dengan endpoint DELETE.  
- Pastikan `app_name` sama dengan folder agent (`jamu_rekomendasi_agent`).  
- Gunakan user/session ID unik saat testing.

