import base64
import hashlib
import uuid

from cryptography.fernet import Fernet


class AdvancedCipher:
    def __init__(self, key, agent):
        self.agent = agent
        self.key_material = hashlib.sha256(str(key).encode("utf-8")).digest()
        self.fernet = Fernet(base64.urlsafe_b64encode(self.key_material))

    def process(self, text):
        payload = self.fernet.encrypt((text or "").encode("utf-8")).decode("utf-8")
        record_id = str(uuid.uuid4())[:8]
        signature = hashlib.sha256(f"{record_id}:{self.agent}:{self.key_material.hex()}".encode("utf-8")).hexdigest()[:12]
        qr_token = f"ID:{record_id}|SIG:{signature}|PAYLOAD:{payload[:32]}"
        return payload, record_id, qr_token
