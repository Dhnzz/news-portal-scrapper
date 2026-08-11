# AGENTS.md

Panduan untuk agen yang bekerja di repo ini. Baca sebelum mengerjakan tugas.

## Konteks

- **Bahasa kerja**: dokumentasi teknis dan komentar kode dalam Bahasa Indonesia bila memungkinkan; istilah teknis tetap Inggris.
- Baca `CONTEXT.md` di root untuk glosarium domain (Artikel, Sumber, Scrape, Ringkasan, Jadwal, Anggota, Admin).
- Ikuti keputusan yang terdokumentasi di `docs/adr/` jika ada.

## Tooling

- Python 3.11+, FastAPI, PostgreSQL.
- LLM: Ollama lokal, model `qwen2.5:3b`.
- Tes: pytest + FastAPI TestClient. Jalankan `pytest` di root untuk seluruh suite.
- Lint/typecheck: gunakan konvensi yang dibentuk ticket scaffold; pastikan `pytest` hijau sebelum selesai.

## Agent skills

### Issue tracker

Issues dan tickets live di GitHub Issues repo ini (dipakai via `gh` CLI). Lihat `docs/agents/issue-tracker.md`.

### Triage labels

Lima label default: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. Lihat `docs/agents/triage-labels.md`.

### Domain docs

Single-context — satu `CONTEXT.md` + `docs/adr/` di root. Lihat `docs/agents/domain.md`.