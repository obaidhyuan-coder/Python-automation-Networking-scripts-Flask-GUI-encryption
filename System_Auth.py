import hashlib
import hmac
import json
import os
from pathlib import Path


DEFAULT_PASSWORD_ENV = "APP_DEFAULT_PASSWORD"


def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)


def _get_default_password() -> str:
    return os.environ.get(DEFAULT_PASSWORD_ENV, "change-me")


class SystemAuth:
    def __init__(self, file_name="security.json", user_name="obaidh"):
        self.max_attempts = 4
        self.file_name = file_name
        self.user_name = user_name
        self._password_hash = ""
        self._password_salt = b""
        self._failed_attempts = 0
        self._is_locked = False
        self._load_security_file()

    def _load_security_file(self):
        if not os.path.exists(self.file_name):
            salt = os.urandom(16)
            default_password = _get_default_password()
            self._password_salt = salt
            self._password_hash = _hash_password(default_password, salt).hex()
            self._failed_attempts = 0
            self._is_locked = False
            self._save_security_file()
            return

        with open(self.file_name, "r", encoding="utf-8") as file:
            data = json.load(file)

        user_data = data.get(self.user_name, {})
        if not user_data:
            self._password_salt = os.urandom(16)
            self._password_hash = _hash_password(_get_default_password(), self._password_salt).hex()
            self._failed_attempts = 0
            self._is_locked = False
            self._save_security_file()
            return

        try:
            self._password_salt = bytes.fromhex(user_data.get("salt", ""))
        except ValueError:
            self._password_salt = os.urandom(16)

        self._password_hash = user_data.get("password_hash", "")
        self._failed_attempts = int(user_data.get("failed_attempts", 0))
        self._is_locked = bool(user_data.get("is_locked", False))

    def _save_security_file(self):
        data = {
            self.user_name: {
                "password_hash": self._password_hash,
                "salt": self._password_salt.hex(),
                "failed_attempts": self._failed_attempts,
                "is_locked": self._is_locked,
            }
        }

        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def set_password(self, new_password: str):
        if not new_password or not isinstance(new_password, str):
            raise ValueError("Password must be a non-empty string")
        self._password_salt = os.urandom(16)
        self._password_hash = _hash_password(new_password, self._password_salt).hex()
        self._failed_attempts = 0
        self._is_locked = False
        self._save_security_file()

    def _verify_password(self, entered_password: str) -> bool:
        candidate = _hash_password(entered_password, self._password_salt)
        return hmac.compare_digest(candidate.hex(), self._password_hash)

    def attempt_login(self, entered_password):
        if self._is_locked:
            return "LOCKED"

        if self._verify_password(entered_password):
            self._failed_attempts = 0
            self._save_security_file()
            return "GRANTED"

        self._failed_attempts += 1
        if self._failed_attempts >= self.max_attempts:
            self._is_locked = True
            self._save_security_file()
            return "LOCKED"

        remaining = self.max_attempts - self._failed_attempts
        self._save_security_file()
        return f"DENIED ({remaining} attempts left)"


if __name__ == "__main__":
    auth = SystemAuth()
    print("Auth ready. Set APP_DEFAULT_PASSWORD to change the initial password.")
