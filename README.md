# Web Scraper Berita + Ringkasan LLM

Aplikasi web multi-user (tim) untuk mengambil berita dari banyak portal berita, menyimpannya dalam satu database bersama, dan meringkas tiap artikel menjadi paragraf Bahasa Indonesia memakai model LLM gratis (Ollama `qwen2.5:3b`) yang berjalan di server.

## Fitur utama

- **Scraping berita** — mengambil artikel dari banyak Sumber (portal berita) ke dalam database.
- **Ringkasan LLM** — ringkasan pendek Bahasa Indonesia (3–5 kalimat) per Artikel, dihasilkan on-demand lalu di-cache.
- **Jadwal otomatis** — scraping terjadwal per Sumber, mati secara default dan dapat diaktifkan per Sumber.
- **Rol pengguna** — Anggota (baca, filter, cari, ringkas, atur Jadwal) dan Admin (mengelola Sumber dan pengguna).

## Arsitektur

- **Backend** — Python, FastAPI, frontend server-rendered.
- **Database** — PostgreSQL.
- **Scraping** — Python + HTTP client.
- **LLM** — Ollama lokal, model `qwen2.5:3b`, ringkasan asynchronous lewat antrean.

## Struktur repository

```
├── CONTEXT.md        # konteks dan glosarium domain
├── AGENTS.md         # panduan untuk agen yang bekerja di repo ini
└── docs/
    ├── adr/          # keputusan arsitektur (jika ada)
    └── agents/       # skill dan workflow agen
```

## Pengembangan

- **Bahasa** — Python 3.11+, FastAPI, PostgreSQL.
- **Tes** — `pytest` + FastAPI TestClient. Jalankan `pytest` di root untuk seluruh suite.
- **LLM lokal** — pastikan Ollama berjalan dan model `qwen2.5:3b` tersedia: `ollama pull qwen2.5:3b`.

> Glosarium istilah domain (Artikel, Sumber, Scrape, Ringkasan, Jadwal, Anggota, Admin) tersedia di `CONTEXT.md`.