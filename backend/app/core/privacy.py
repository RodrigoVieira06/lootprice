import hashlib

from app.core.config import get_settings


def hash_ip_address(ip_address: str, salt: str | None = None) -> str:
    hash_salt = salt if salt is not None else get_settings().ip_hash_salt
    if not hash_salt:
        raise ValueError("IP_HASH_SALT must be configured to hash IP addresses")

    payload = f"{hash_salt}:{ip_address}".encode()
    return hashlib.sha256(payload).hexdigest()
