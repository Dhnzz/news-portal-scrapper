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

- App: http://localhost:8000 — healthcheck di http://localhost:8000/health (memverifikasi koneksi DB), login di http://localhost:8000/login.
- PostgreSQL: localhost:5432 (user `news`, password `news`, db `news`).

Service `migrate` menjalankan `alembic upgrade head` lalu `python -m app.cli seed-admin` — otomatis membuat akun admin awal. Default `admin` / `admin123`; ganti lewat env `ADMIN_USERNAME`/`ADMIN_PASSWORD` di `.env`.

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

Migrasi memakai Alembic. Tabel `users` menyimpan password sebagai hash PBKDF2-SHA256, bukan plaintext.

```sh
alembic revision --autogenerate -m "pesan"   # buat migrasi baru
alembic upgrade head                          # terapkan
alembic downgrade -1                          # balik satu langkah
```

## Akun admin awal

Seed admin dibuat lewat CLI (idempoten — dilewati bila user sudah ada):

```sh
python -m app.cli seed-admin
python -m app.cli seed-admin --username boss --password "rahasia-super"
```

Default `admin` / `admin123` (ada peringatan di stderr); override via `ADMIN_USERNAME`/`ADMIN_PASSWORD` atau argumen `--username`/`--password`.

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

- `app/` — aplikasi FastAPI (`config.py` baca konfigurasi dari env, `db.py` engine/sesi async, `models.py` model SQLAlchemy, `security.py` hash password + session cookie, `deps.py` dependensi auth, `routers/` berisi `health.py`, `auth.py` (login/logout/beranda), `admin.py` (kelola user), `cli.py` utilitas CLI, `templates/` halaman login/beranda/admin).
- `alembic/` — migrasi database.
- `tests/` — suite pytest.
- `docker-compose.yml` — Postgres dev (`dev`), Postgres test (`test`), app, dan service `migrate`.
