import json
import os
import shutil
from datetime import datetime


class VaultManager:
    def __init__(self, process_type="enc"):
        self.ptype = process_type
        self.vault_file = "central_vault.json"
        self.backup_folder = "vault_backups"

        os.makedirs(self.backup_folder, exist_ok=True)
        if not os.path.exists(self.vault_file):
            with open(self.vault_file, "w", encoding="utf-8") as file:
                json.dump([], file)

    def _load_records(self):
        try:
            with open(self.vault_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return []

    def read_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def save_file(self, original_path, secret_content, tag="secured"):
        name, extension = os.path.splitext(original_path)
        if name.endswith("_secured") or name.endswith("_restored"):
            name = name[:-8]

        new_path = f"{name}_{tag}{extension}"
        with open(new_path, "w", encoding="utf-8") as file:
            file.write(secret_content)
        self.save_record({"source": original_path, "tag": tag, "status": "ACTIVE"})
        return new_path

    def save_record(self, record_content, status="ACTIVE"):
        if isinstance(record_content, dict):
            payload = record_content.copy()
            payload.setdefault("status", status)
            payload.setdefault("created_at", datetime.now().isoformat())
            payload.setdefault("vault_id", os.urandom(4).hex())
        else:
            payload = {
                "content_summary": str(record_content)[:30] + "...",
                "status": status,
                "created_at": datetime.now().isoformat(),
                "vault_id": os.urandom(4).hex(),
            }

        data = self._load_records()
        data.append(payload)

        with open(self.vault_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return self.backup_vault()

    def is_expired(self, created_at_str, days_limit=30):
        created_at = datetime.fromisoformat(created_at_str)
        age = datetime.now() - created_at
        return age.days >= days_limit

    def backup_vault(self):
        os.makedirs(self.backup_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_folder, f"backup_vault_{timestamp}.json")
        shutil.copy2(self.vault_file, backup_path)
        return f"Backup created: {timestamp}"
