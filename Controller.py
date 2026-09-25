import base64
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

import qrcode

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
        key_input = self.view.ent_key.get().strip()
        try:
            if not key_input:
                raise ValueError
            return key_input
        except (ValueError, TypeError):
            messagebox.showwarning("SECURITY WARNING", "Invalid key provided. Please enter a non-empty value.")
            return None

    def encrypt_text(self):
        text = self.view.ent_msg.get()
        key = self.get_key()
        if text and key:
            cipher = self._build_fernet()
            encrypted = cipher.encrypt(text.encode("utf-8")).decode("utf-8")
            self.view.ent_msg.delete(0, "end")
            self.view.ent_msg.insert(0, encrypted)
            self.view.ent_msg.config(fg="#00ff00")

    def decrypt_text(self):
        text = self.view.ent_msg.get()
        key = self.get_key()
        if text and key:
            try:
                cipher = self._build_fernet()
                decrypted = cipher.decrypt(text.encode("utf-8")).decode("utf-8")
                self.view.ent_msg.delete(0, "end")
                self.view.ent_msg.insert(0, decrypted)
                self.view.ent_msg.config(fg="#38bdf8")
            except Exception:
                messagebox.showerror("Decrypt failed", "The message could not be decrypted with the supplied key.")

    def file_encrypt(self):
        key = self.get_key()
        if not key:
            return
        path = filedialog.askopenfilename(title="SECURE EXTERNAL FILE")
        if path:
            try:
                cipher = self._build_fernet()
                with open(path, "rb") as file:
                    content = file.read()
                encrypted = cipher.encrypt(content)
                new_path = self.vault.save_file(path, encrypted.decode("utf-8"), "secured")
                self.view.lbl_output.config(text=f"FILE SECURED: {new_path}", fg="#00ff00")
            except Exception as exc:
                messagebox.showerror("File encryption failed", str(exc))

    def file_decrypt(self):
        key = self.get_key()
        if not key:
            return
        path = filedialog.askopenfilename(title="RESTORE EXTERNAL FILE")
        if path:
            try:
                cipher = self._build_fernet()
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                decrypted = cipher.decrypt(content.encode("utf-8"))
                new_path = self.vault.save_file(path, decrypted.decode("utf-8"), "restored")
                self.view.lbl_output.config(text=f"FILE RESTORED: {new_path}", fg="#38bdf8")
            except Exception as exc:
                messagebox.showerror("File decryption failed", str(exc))

    def export_qr(self):
        text = self.view.ent_msg.get()
        key = self.get_key()
        if not text or not key:
            return

        engine = AdvancedCipher(key, "Agent_007")
        enc, record_id, qr_token = engine.process(text)
        self.vault.save_record({
            "id": record_id,
            "agent": "Agent_007",
            "status": "ACTIVE",
        })
        img = qrcode.make(qr_token)
        img.save("access_token.png")
        self.view.show_image("access_token.png")
