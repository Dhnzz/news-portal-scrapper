# Context — Web Scraper Berita + Ringkasan LLM

## Ringkasan

Aplikasi web multi-user (tim) untuk mengambil berita dari banyak portal, menyimpannya dalam satu database bersama, dan meringkas tiap artikel menjadi paragraf Bahasa Indonesia memakai model LLM gratis (Ollama `qwen2.5:3b`) yang berjalan di server.

## Glosarium

- **Artikel** — unit konten yang diambil dari portal berita: judul, URL, penulis, waktu terbit, teks penuh, gambar. Teridentifikasi unik berdasarkan **URL**.
- **Sumber** — satu portal berita yang di-parse, contoh: detik, kompas, tempo. Setiap **Sumber** punya parser sendiri dan bisa diaktifkan/dimatikan jadwalnya secara terpisah.
- **Scrape** — tindakan mengambil artikel dari sebuah **Sumber** ke dalam database.
- **Ringkasan** — paragraf pendek Bahasa Indonesia (3–5 kalimat) dari sebuah **Artikel**, dihasilkan oleh LLM pada permintaan manual, lalu di-cache.
- **Jadwal** — pengaturan scraping otomatis per **Sumber**, mati secara default, dapat diaktifkan/dinonaktifkan oleh anggota.
- **Anggota** — pengguna dengan peran baca, filter, cari, ringkas, dan atur **Jadwal**.
- **Admin** — pengguna yang selain hak **Anggota**, juga mengelola **Sumber** dan pengguna lain.

## Keputusan arsitektur

- Backend Python (FastAPI), frontend server-rendered.
- PostgreSQL sebagai penyimpanan; Python + HTTP client untuk scraping.
- LLM: Ollama lokal, model `qwen2.5:3b`, ringkasan asynchronous lewat antrean.