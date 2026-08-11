# News Portal Scraper

Web scraper berita + ringkasan LLM. Backend FastAPI + PostgreSQL, ringkasan via Ollama `qwen2.5:3b` (tiket berikutnya).

## Prasyarat

- Python 3.11+
- Docker Desktop (untuk `docker compose`)

## Menjalankan aplikasi (profil dev)

```sh
cp .env.example .env   # sesuaikan jika perlu
docker compose --profile dev up --build
```

- App: http://localhost:8000 — healthcheck di http://localhost:8000/health (memverifikasi koneksi DB).
- PostgreSQL: localhost:5432 (user `news`, password `news`, db `news`).

## Menjalankan tanpa Docker

```sh
python -m venv .venv
.venv\Scripts\pip install -e ".[dev]"     # Windows
# aktifkan venv, lalu:
alembic upgrade head
uvicorn app.main:app --reload
```

Atur `DATABASE_URL` dan `SECRET_KEY` lewat environment (contoh di `.env.example`).

## Migrasi DB

Migrasi memakai Alembic; skema awal masih kosong.

```sh
alembic revision --autogenerate -m "pesan"   # buat migrasi baru
alembic upgrade head                          # terapkan
alembic downgrade -1                          # balik satu langkah
```

## Tes

```sh
pytest
```

Suite memakai DB test terpisah (`TEST_DATABASE_URL`, host port `5433` — jangan tertukar dengan DB dev di `5432`). Untuk menjalankan Postgres test:

```sh
docker compose --profile test up -d test-db
pytest
```

## Struktur

- `app/` — aplikasi FastAPI (`config.py` baca konfigurasi dari env, `db.py` engine/sesi async, `routers/health.py` healthcheck).
- `alembic/` — migrasi database.
- `tests/` — suite pytest.
- `docker-compose.yml` — Postgres dev (`dev`), Postgres test (`test`), app, dan service `migrate`.
