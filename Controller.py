import base64
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

import qrcode
from cryptography.fernet import Fernet

from AdvancedCipher import AdvancedCipher
from Vault import VaultManager


class CipherController:
    def __init__(self, view, engine):
        self.view = view
        self.engine = engine
        self.vault = VaultManager("enc")
        self.view.btn_enc.config(command=self.encrypt_text)
        self.view.btn_dec.config(command=self.decrypt_text)
        self.view.btn_f_enc.config(command=self.file_encrypt)
        self.view.btn_f_dec.config(command=self.file_decrypt)
        self.view.btn_exp.config(command=self.export_qr)

    def _build_fernet(self):
        key_input = self.view.ent_key.get().strip()
        if not key_input:
            raise ValueError("A key is required")
        key_material = hashlib.sha256(key_input.encode("utf-8")).digest()
        return Fernet(base64.urlsafe_b64encode(key_material))

    def get_key(self):
        key = self.view.ent_key.get().strip()
        if not key:
            messagebox.showwarning("Missing key", "Enter a non-empty encryption key.")
            return None
        return key

    def encrypt_text(self):
        text, key = self.view.ent_msg.get(), self.get_key()
        if text and key:
            encrypted = self._build_fernet().encrypt(text.encode()).decode()
            self.view.ent_msg.delete(0, "end")
            self.view.ent_msg.insert(0, encrypted)
            self.view.ent_msg.config(fg="#00ff00")

    def decrypt_text(self):
        text, key = self.view.ent_msg.get(), self.get_key()
        if text and key:
            try:
                decrypted = self._build_fernet().decrypt(text.encode()).decode()
                self.view.ent_msg.delete(0, "end")
                self.view.ent_msg.insert(0, decrypted)
                self.view.ent_msg.config(fg="#38bdf8")
            except Exception:
                messagebox.showerror("Decrypt failed", "The key or encrypted text is invalid.")

    def file_encrypt(self):
        key = self.get_key()
        path = filedialog.askopenfilename(title="Encrypt file") if key else None
        if not path:
            return
        try:
            with open(path, "rb") as file:
                encrypted = self._build_fernet().encrypt(file.read())
            new_path = self.vault.save_file(path, encrypted.decode(), "secured")
            self.view.lbl_output.config(text=f"File secured: {new_path}", fg="#00ff00")
        except OSError as exc:
            messagebox.showerror("File encryption failed", str(exc))

    def file_decrypt(self):
        key = self.get_key()
        path = filedialog.askopenfilename(title="Restore file") if key else None
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as file:
                decrypted = self._build_fernet().decrypt(file.read().encode())
            new_path = self.vault.save_file(path, decrypted.decode(), "restored")
            self.view.lbl_output.config(text=f"File restored: {new_path}", fg="#38bdf8")
        except (OSError, ValueError):
            messagebox.showerror("File decryption failed", "The file or key is invalid.")

    def export_qr(self):
        text, key = self.view.ent_msg.get(), self.get_key()
        if not text or not key:
            return
        _, record_id, qr_token = AdvancedCipher(key, "local-demo").process(text)
        self.vault.save_record({"id": record_id, "agent": "local-demo", "status": "ACTIVE"})
        qrcode.make(qr_token).save("access_token.png")
        self.view.show_image("access_token.png")
