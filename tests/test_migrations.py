import subprocess
import sys


def test_alembic_offline_migration_generates_users_schema():
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head", "--sql"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "INSERT INTO alembic_version" in result.stdout
    assert "CREATE TABLE alembic_version" in result.stdout
    # Alembic version + tabel users (model yang terdaftar di Base.metadata).
    assert result.stdout.count("CREATE TABLE") == 2
    assert "CREATE TABLE users" in result.stdout