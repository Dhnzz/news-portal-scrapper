import subprocess
import sys


def test_alembic_offline_migration_generates_empty_schema():
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head", "--sql"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    # Skema awal kosong: hanya tabel versi alembic, tanpa tabel domain lain.
    assert "INSERT INTO alembic_version" in result.stdout
    assert "CREATE TABLE alembic_version" in result.stdout
    assert result.stdout.count("CREATE TABLE") == 1