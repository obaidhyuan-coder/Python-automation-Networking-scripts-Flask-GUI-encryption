import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from Caesar import CaesarCipher
from Vault import VaultManager
from AdvancedCipher import AdvancedCipher

class CipherController:
    def __init__(self, view, engine):
        self.view = view
        self.engine = engine
       
        self.vault = VaultManager('enc') 

        self.view.btn_enc.config(command=self.encrypt_text)
        self.view.btn_dec.config(command=self.decrypt_text)
        self.view.btn_f_enc.config(command=self.file_encrypt)
        self.view.btn_f_dec.config(command=self.file_decrypt)
        self.view.btn_exp.config(command=self.export_qr)

    def get_key(self):
        key_input = self.view.ent_key.get()
        
        try:
           
            if not key_input.strip():
                raise ValueError
            return int(key_input)
            
        except (ValueError, TypeError):
           
            messagebox.showwarning("SECURITY WARNING", "Invalid key provided. Defaulting to 0.")
            return 0

    def encrypt_text(self):
        text = self.view.ent_msg.get()
        key = self.get_key()
        if text and key is not None:
            cipher = CaesarCipher(key)
            res = cipher.encrypt(text)
            self.view.ent_msg.delete(0, "end")
            self.view.ent_msg.insert(0,res)
            self.view.ent_msg.config(fg="#00ff00")


    def decrypt_text(self):
       
        text = self.view.ent_msg.get()
        key = self.get_key()
        if text and key is not None:
            cipher = CaesarCipher(key)
            res = cipher.decrypt(text)
            self.view.ent_msg.delete(0,"end")
            self.view.ent_msg.insert(0,res)
            self.view.ent_msg.config(fg="#38bdf8")

    def file_encrypt(self):
        key = self.get_key()
        path = filedialog.askopenfilename(title="SECURE EXTERNAL FILE")
        if path and key:
            content = self.vault.read_file(path)
            cipher = CaesarCipher(key)
            enc_data = cipher.encrypt(content)
            
           
            new_path = self.vault.save_file(path, enc_data, "secured")
            
            self.view.lbl_output.config(text=f"FILE SECURED: {new_path}",fg="#00ff00")

    def file_decrypt(self):
        key = self.get_key()
        path = filedialog.askopenfilename(title="RESTORE EXTERNAL FILE")
        if path and key:
            content = self.vault.read_file(path)
            cipher = CaesarCipher(key)
            dec_data = cipher.decrypt(content)
            
          
            new_path = self.vault.save_file(path, dec_data, "restored")
            
            self.view.lbl_output.config(text=f"FILE RESTORED: {new_path}",fg="#38bdf8")

    def export_qr(self):
      text = self.view.ent_msg.get()
      key = self.get_key()

      engine = AdvancedCipher(key, "Agent_007")
      enc, record_id, qr_token = engine.process(text)
      vault = VaultManager("Secure")
      vault.save_record({
                             "id": record_id,
                             "key": key,
                             "agent": "Agent_007"
                        })
      img = qrcode.make(qr_token)
      img.save("access_token.png")
      self.view.show_image("access_token.png")
      print(f"System: Record {record_id} saved. QR Generated.")
