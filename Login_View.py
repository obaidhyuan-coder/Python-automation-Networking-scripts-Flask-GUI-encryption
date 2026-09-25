import tkinter as tk
from tkinter import messagebox
import winsound
from System_Auth import SystemAuth
class LoginWindow:
 def __init__(self, root):
  self.root = root
  self.root.title("Cyber-Guard Auth")
  self.root.geometry("400x250")
  self.root.configure(bg="black")
  self.auth_system = SystemAuth()
  self.is_authenticated = False
  tk.Label(root, text="SYSTEM LOCKED", bg="black", fg="#00FF00", font=("Consolas", 18,
          "bold")).pack(pady=20)
  self.ent_pass = tk.Entry(root, show="*", width=20, font=("Consolas", 14), bg="#222",
                                                                                fg="#00FF00")
  self.ent_pass.pack(pady=10)
  self.btn_login = tk.Button(root, text="AUTHENTICATE", bg="#00FF00", fg="black", font=
           ("Consolas", 12, "bold"),command=self.check_login)



  self.btn_login.pack(pady=10)
  self.lbl_status = tk.Label(root, text="Enter Password...", bg="black", fg="#00FF00", font=
   ("Consolas", 10))
  self.lbl_status.pack(pady=5)

 def check_login(self):
  attempt = self.ent_pass.get()
  result = self.auth_system.attempt_login(attempt)
  if result == "GRANTED":
     self.is_authenticated= True
     messagebox.showinfo("Access Granted", "Welcome to cyber_encryption_station.")
     self.root.destroy()
  elif result == "LOCKED":
   self.trigger_panic_mode()
  else:
   self.lbl_status.config(text=result, fg="red")
 def trigger_panic_mode(self):
  self.root.configure(bg="red")
  self.lbl_status.config(text="INTRUDER DETECTED! SYSTEM LOCKDOWN!", fg="white",
        bg="red",font=("Consolas", 12, "bold"))


  self.btn_login.config(state="disabled")
  self.ent_pass.config(state="disabled")
  winsound.Beep(1000, 500)
  winsound.Beep(1000, 500)
