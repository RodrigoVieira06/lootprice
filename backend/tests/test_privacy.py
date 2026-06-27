import pytest

from app.core.privacy import hash_ip_address


def test_hash_ip_address_is_deterministic_and_irreversible() -> None:
    ip_hash = hash_ip_address("203.0.113.10", salt="test-salt")

    assert ip_hash == hash_ip_address("203.0.113.10", salt="test-salt")
    assert ip_hash != hash_ip_address("203.0.113.11", salt="test-salt")
    assert ip_hash != "203.0.113.10"
    assert "203.0.113.10" not in ip_hash
    assert len(ip_hash) == 64


def test_hash_ip_address_requires_salt() -> None:
    with pytest.raises(ValueError, match="IP_HASH_SALT"):
        hash_ip_address("203.0.113.10", salt="")
