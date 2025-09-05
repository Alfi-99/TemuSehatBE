# TemuSehat Agent (ADK) – Railway Deployment Guide

## Deskripsi
Ini adalah panduan untuk menjalankan agent **`jamu_rekomendasi_agent`** menggunakan **ADK API Server** yang sudah dideploy di **Railway**. Panduan ini mencakup: setup, start session, kirim pesan, dan end session.

---

## 1 API Endpoints

Railway URL: `https://temusehatbe-production.up.railway.app`

| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/apps/{app_name}/users/{user_id}/sessions/{session_id}` | POST | Buat / start session |
| `/run` | POST | Kirim pesan ke agent (ask) |
| `/apps/{app_name}/users/{user_id}/sessions/{session_id}` | DELETE | Hapus / end session |

---

## 2 PowerShell cURL Commands

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

## 4 Testing / Debugging

1. Setelah server jalan, buka **Swagger UI**:
```
https://temusehatbe-production.up.railway.app/docs
```

2. Bisa langsung test endpoint dari browser.

---

## 6 Tips

- Jika muncul `Session already exists`, hapus session dulu dengan endpoint DELETE.  
- Pastikan `app_name` sama dengan folder agent (`jamu_rekomendasi_agent`).  
- Gunakan user/session ID unik saat testing.

