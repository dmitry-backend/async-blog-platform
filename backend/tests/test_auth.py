import pytest
from app.auth.security import hash_password, verify_password, create_access_token, decode_access_token
from app.auth.validators import validate_email, validate_password

def test_password_hash():
    pwd = "StrongPass1!"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_token():
    data = {"sub": "1", "role": "user"}
    token = create_access_token(data)
    decoded = decode_access_token(token)
    assert decoded["sub"] == "1"
    assert decoded["role"] == "user"

def test_validators():
    assert validate_password("StrongPass1!")
    assert not validate_password("weak")
    assert validate_email("user@test.com")
    assert not validate_email("bad-email")
