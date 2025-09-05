# TemuSehat Chatbot PHP Client

Repo ini berisi contoh **PHP client** untuk berinteraksi dengan **FastAPI TemuSehat Chatbot** yang sudah dideploy di [Railway](https://temusehat-production.up.railway.app).  

Client ini mendukung tiga endpoint utama:

1. **Create Session** – Membuat session baru.
2. **Ask Agent** – Mengirim keluhan/pesan ke chatbot.
3. **End Session** – Mengakhiri session.

Output dari semua fungsi berupa **JSON**.

---

## 📦 Struktur File

```
temusehat-php-client/
│
├─ temusehat_client.php   # Script PHP untuk create/ask/end session
└─ README.txt             # Dokumentasi ini
```

---

## ⚙️ Setup

1. Pastikan **PHP sudah terinstall** di sistem kamu.  
   Cek dengan:

   ```powershell
   php -v
   ```

2. Simpan file `temusehat_client.php` di folder pilihanmu.  
3. Pastikan komputer/PowerShell bisa mengakses internet untuk reach API Railway.

---

## 💻 Contoh Kode

```php
<?php
include 'temusehat_client.php'; // Jika dipisah file

$user_id = "user123";
$session_id = "sess123";

// 1️⃣ Create session
$response_create = create_session($user_id, $session_id);
print_r(json_decode($response_create, true));

// 2️⃣ Ask agent
$response_ask = ask_agent($user_id, $session_id, "Saya batuk kering");
print_r(json_decode($response_ask, true));

// 3️⃣ End session
$response_end = end_session($user_id, $session_id);
print_r(json_decode($response_end, true));
?>
```

---

## 🚀 Menjalankan Script di PowerShell

1. Buka PowerShell.  
2. Arahkan ke folder tempat file PHP kamu disimpan.  
3. Jalankan perintah:

```powershell
php temusehat_client.php
```

Output akan berupa **JSON**, contohnya:

```json
{
    "create_session": {
        "message": "Session created",
        "session": {
            "user_id": "user123",
            "state": {"status": "active"},
            "history": []
        }
    },
    "ask_agent": {
        "reply": {
            "type": "rule",
            "rekomendasi": "Rebusan kunyit + madu atau daun sirih bagus untuk batuk kering."
        },
        "session": {
            "user_id": "user123",
            "state": {"status": "active"},
            "history": [
                {"role": "user", "content": "Saya batuk kering"},
                {"role": "agent", "content": { "type": "rule", "rekomendasi": "..."}}
            ]
        }
    },
    "end_session": {
        "message": "Session ended",
        "session": {
            "user_id": "user123",
            "state": {"status": "ended"},
            "history": [...]
        }
    }
}
```

---

## 🔧 Tips

- Pastikan **session_id unik** untuk setiap user agar history tidak tumpang tindih.  
- Semua request menggunakan **POST JSON**.  
- Bisa integrasikan ke frontend PHP atau framework lain (Laravel, CodeIgniter, dll).  

---

## 📌 Link Endpoint

- Base URL: `https://temusehat-production.up.railway.app`  
- `/create_session` – Membuat session baru  
- `/ask` – Kirim keluhan/pesan ke chatbot  
- `/end_session` – Akhiri session

