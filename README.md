# 🍃 Herbal AI Agent

AI Agent ini adalah **teman pintar** yang bisa memberikan rekomendasi jamu/herbal untuk **keluhan kesehatan ringan**. Agent juga otomatis mendeteksi **red flag** (indikator penyakit serius) dan menyarankan pengguna untuk konsultasi ke dokter.

---

## 🚀 Fitur Utama

1. **Konsultasi Semi-Interaktif**

   * Kalau user bilang *"batuk"* → agent tidak langsung jawab.
   * Agent akan **gali informasi tambahan**: durasi, gejala lain, sifat keluhan (kering/berdahak, dll).
   * Baru kasih rekomendasi jamu/herbal yang lebih akurat.

2. **Red Flag Detector**

   * Kalau keluhan menunjukkan tanda penyakit serius (contoh: nyeri dada, sesak napas, pingsan, demam tinggi berkepanjangan, dsb), agent langsung:

     ```json
     {
       "status": "red_flag",
       "message": "Segera konsultasi dokter"
     }
     ```
   * Frontend bisa munculin indikator khusus (misalnya alert merah).

3. **Mode Edukatif & Ramah**

   * Penjelasan ringan, semi-edukatif, bukan *dry medical text*.
   * Lebih ke *teman ngobrol pintar* yang nyaranin jamu/herbal + gaya hidup sehat.

---

## 🛠️ Struktur Kode

### File: `agent.py`

* **`rekomendasi_jamu(keluhan: str)`**
  Fungsi yang mengembalikan rekomendasi jamu/herbal, atau meminta klarifikasi kalau informasi belum cukup.

* **`root_agent`**
  Definisi agent berbasis `google.adk.agents.Agent`.

  * `model` → pakai `gemini-2.0-flash`.
  * `tools` → daftar fungsi (saat ini `rekomendasi_jamu`).
  * `instruction` → prompt yang mengatur cara agent berinteraksi.

---

## 📡 Alur Kerja (Frontend ↔ Backend ↔ Agent)

1. **User input** → misalnya `"Saya pusing sejak kemarin sore"`.
2. **Backend** → diteruskan ke `root_agent`.
3. **Agent**:

   * Kalau info masih minim → balikin pertanyaan klarifikasi (`status: "clarify"`).
   * Kalau cukup detail → balikin rekomendasi jamu/herbal (`status: "success"`).
   * Kalau gejala berbahaya → balikin red flag (`status: "red_flag"`).
4. **Frontend**:

   * Render jawaban agent di chat bubble.
   * Kalau ada `clarify_message`, tampilkan pertanyaan balik.
   * Kalau `red_flag`, munculkan notifikasi/alert.

---

## 📋 Contoh Response

### ✅ Rekomendasi Jamu

Input:

```text
Saya batuk kering sudah 3 hari
```

Output:

```json
{
  "status": "success",
  "rekomendasi": "Rebusan kunyit + madu atau daun sirih bagus untuk batuk kering."
}
```

### ❓ Klarifikasi

Input:

```text
Saya batuk
```

Output:

```json
{
  "status": "clarify",
  "clarify_message": "Bisa ceritakan lebih detail tentang batuknya? Apakah kering atau berdahak? Sudah berapa lama?"
}
```

### 🚨 Red Flag

Input:

```text
Dada saya terasa sesak dan nyeri sampai lengan kiri
```

Output:

```json
{
  "status": "red_flag",
  "message": "Segera konsultasi dokter"
}
```

---

## 💡 Catatan untuk Dev

* Agent **tidak dimaksudkan sebagai pengganti dokter**.
* Harus ada **disclaimer** di frontend (misalnya “Informasi ini hanya bersifat edukasi dan bukan diagnosis medis”).
* Kalau mau scaling, bikin mapping **gejala → jamu** di database / knowledge base, biar nggak stuck di `if-else`.

---
