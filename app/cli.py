from __future__ import annotations

import argparse
import asyncio
import os
import sys

from app.config import Settings
from app.db import close_db, get_sessionmaker, init_db
from app.users import create_user, fetch_user_by_username

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"


async def seed_admin(username: str, password: str) -> None:
    async with get_sessionmaker()() as session:
        if await fetch_user_by_username(session, username) is not None:
            print(f"Admin '{username}' sudah ada; dilewati.")
            return
        await create_user(session, username, password, role="admin")
        await session.commit()
        print(f"Admin '{username}' dibuat.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m app.cli", description="Utilitas CLI aplikasi."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    seed = sub.add_parser("seed-admin", help="Buat akun admin awal (idempoten).")
    seed.add_argument(
        "--username", default=os.environ.get("ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME)
    )
    seed.add_argument(
        "--password", default=os.environ.get("ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)
    )
    args = parser.parse_args(argv)

    if args.command == "seed-admin":
        if args.password == DEFAULT_ADMIN_PASSWORD:
            print(
                "PERINGATAN: memakai password admin bawaan ('admin123'); "
                "ganti lewat --password atau env ADMIN_PASSWORD.",
                file=sys.stderr,
            )
        init_db(Settings())
        try:
            asyncio.run(seed_admin(args.username, args.password))
        finally:
            asyncio.run(close_db())
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())