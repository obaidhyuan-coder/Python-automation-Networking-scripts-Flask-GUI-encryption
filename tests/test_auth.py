import os
from pathlib import Path

import pytest

from System_Auth import SystemAuth
from Vault import VaultManager


def test_password_hash_roundtrip(tmp_path):
    security_file = tmp_path / "security.json"
    auth = SystemAuth(file_name=str(security_file), user_name="obaidh")
    auth.set_password("demo-password")
    assert auth.attempt_login("demo-password") == "GRANTED"


def test_lockout_behavior(tmp_path):
    security_file = tmp_path / "security.json"
    auth = SystemAuth(file_name=str(security_file), user_name="obaidh")
    auth.set_password("demo-password")
    auth.attempt_login("wrong")
    auth.attempt_login("wrong")
    auth.attempt_login("wrong")
    assert auth.attempt_login("demo-password") == "LOCKED"


def test_vault_can_store_record(tmp_path):
    old_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        vault = VaultManager("enc")
        result = vault.save_record({"status": "ACTIVE", "demo": True})
        assert isinstance(result, str)
        assert (tmp_path / "central_vault.json").exists()
    finally:
        os.chdir(old_cwd)
