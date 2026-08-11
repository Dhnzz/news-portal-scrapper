from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time

# Iterasi PBKDF2-SHA256; dapat diturunkan lewat env agar suite tes cepat.
PBKDF2_ITERATIONS = int(os.environ.get("PASSWORD_HASH_ITERATIONS", "100000"))

SESSION_COOKIE_NAME = "news_session"
SESSION_TTL_SECONDS = 7 * 24 * 60 * 60


def hash_password(password: str, *, iterations: int = PBKDF2_ITERATIONS) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = stored.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        iteration = int(iterations)
    except (ValueError, AttributeError, TypeError):
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iteration)
    return hmac.compare_digest(actual, expected)


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_session_token(
    user_id: int, secret_key: str, *, ttl: int = SESSION_TTL_SECONDS
) -> str:
    payload = json.dumps(
        {"uid": user_id, "exp": int(time.time()) + ttl}, separators=(",", ":")
    ).encode()
    payload_b64 = _b64url_encode(payload)
    signature = hmac.new(secret_key.encode(), payload_b64.encode(), hashlib.sha256).digest()
    return f"{payload_b64}.{_b64url_encode(signature)}"


def read_session_token(token: str | None, secret_key: str) -> dict | None:
    if not token:
        return None
    try:
        payload_b64, signature_b64 = token.split(".", 1)
    except ValueError:
        return None
    try:
        supplied = _b64url_decode(signature_b64)
        payload = json.loads(_b64url_decode(payload_b64))
    except Exception:
        return None
    expected = hmac.new(secret_key.encode(), payload_b64.encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(expected, supplied):
        return None
    if int(payload.get("exp", 0)) < time.time():
        return None
    return payload