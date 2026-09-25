"""Small local password-hash demonstration.

This is not a full password manager or encrypted vault. The JSON file protects
password verifiers, not the service credentials themselves.
"""

from base64 import b64decode, b64encode
from getpass import getpass
import hashlib
import hmac
import json
import os
from pathlib import Path

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000
SALT_BYTES = 16


def hash_password(password: str, salt: bytes | None = None) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")
    salt = salt or os.urandom(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    return f"{ALGORITHM}${ITERATIONS}${b64encode(salt).decode()}${b64encode(digest).decode()}"


def _verify(stored: str, password: str) -> bool:
    try:
        algorithm, iterations, salt_text, digest_text = stored.split("$", 3)
        if algorithm != ALGORITHM:
            return False
        salt = b64decode(salt_text.encode(), validate=True)
        expected = b64decode(digest_text.encode(), validate=True)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def _load(db_file: str | Path) -> dict[str, str]:
    path = Path(db_file)
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    return data if isinstance(data, dict) else {}


def store_password(service: str, password: str, db_file: str = "passwords.json") -> None:
    if not service.strip():
        raise ValueError("service must not be empty")
    db = _load(db_file)
    db[service] = hash_password(password)
    path = Path(db_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(db, file, indent=2)
    try:
        path.chmod(0o600)
    except OSError:
        pass


def verify_password(service: str, password: str, db_file: str = "passwords.json") -> bool:
    stored = _load(db_file).get(service)
    return bool(stored and _verify(stored, password))


def list_services(db_file: str = "passwords.json") -> list[str]:
    return sorted(_load(db_file))


def main() -> None:
    print("Password Manager (local hash demo)")
    action = input("(1) Store, (2) Verify, (3) List services: ").strip()
    if action == "1":
        service = input("Service name: ").strip()
        password = getpass("Password: ")
        store_password(service, password)
        print("Password verifier stored.")
    elif action == "2":
        service = input("Service name: ").strip()
        print("Correct" if verify_password(service, getpass("Password: ")) else "Incorrect")
    elif action == "3":
        print("\n".join(list_services()) or "No services stored")
    else:
        print("Invalid action")


if __name__ == "__main__":
    main()
