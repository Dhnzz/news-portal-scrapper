from app.security import (
    create_session_token,
    hash_password,
    read_session_token,
    verify_password,
)


def test_hash_password_roundtrip():
    stored = hash_password("rahasia123")
    assert stored != "rahasia123"
    assert stored.startswith("pbkdf2_sha256$")
    assert verify_password("rahasia123", stored)


def test_verify_password_rejects_wrong_password():
    stored = hash_password("rahasia123")
    assert not verify_password("salah", stored)


def test_hash_uses_random_salt():
    assert hash_password("rahasia123") != hash_password("rahasia123")


def test_verify_password_rejects_malformed_hash():
    assert not verify_password("x", "bukan-hash")
    assert not verify_password("x", "")


def test_session_token_roundtrip():
    token = create_session_token(42, "secret")
    payload = read_session_token(token, "secret")
    assert payload is not None
    assert payload["uid"] == 42


def test_session_token_rejects_wrong_secret():
    token = create_session_token(42, "secret")
    assert read_session_token(token, "lain") is None


def test_session_token_rejects_tampered_payload():
    token = create_session_token(42, "secret")
    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")
    assert read_session_token(tampered, "secret") is None


def test_session_token_rejects_expired():
    token = create_session_token(42, "secret", ttl=-10)
    assert read_session_token(token, "secret") is None


def test_session_token_rejects_garbage():
    assert read_session_token("bukan-token", "secret") is None
    assert read_session_token(None, "secret") is None