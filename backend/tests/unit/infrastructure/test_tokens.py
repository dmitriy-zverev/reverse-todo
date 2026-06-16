from reverse_todo.infrastructure.auth.tokens import create_access_token, decode_access_token
from uuid import uuid4


def test_token_roundtrip():
    uid = uuid4()
    token = create_access_token(uid)
    assert decode_access_token(token) == uid


def test_token_invalid():
    assert decode_access_token("not-a-token") is None
