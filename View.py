import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class CipherView:
    def __init__(self, root):
        self.root = root
        self.root.title("cyber_encryption_station")
        self.root.geometry("550x850")     
        self.root.configure(bg="#0f172a") 

      
        self.label_style = {"bg": "#0f172a", "fg": "#38bdf8", "font": ("Segoe UI", 10, "bold")}
        self.entry_style = {"bg": "#1e293b", "fg": "#f1f5f9", "insertbackground": "#38bdf8", 
                            "font": ("Segoe UI", 11), "borderwidth": 0, "highlightthickness": 1, 
                            "highlightbackground": "#334155"}
        self.btn_style = {"bg": "#0ea5e9", "fg": "#ffffff", "font": ("Segoe UI", 10, "bold"), 
                          "activebackground": "#38bdf8", "borderwidth": 0, "cursor": "hand2", "width": 18}
        tk.Label(self.root, text="NETWORK SECURITY OVERRIDE", bg="#0f172a", fg="#f1f5f9", 
                 font=("Segoe UI", 14, "bold")).pack(pady=20)

     
        tk.Label(self.root, text="DATA PAYLOAD", **self.label_style).pack(anchor="w", padx=60)
        self.ent_msg = tk.Entry(self.root, width=40, **self.entry_style)
        self.ent_msg.pack(pady=8)

        tk.Label(self.root, text="ENCRYPTION KEY", **self.label_style).pack(anchor="w", padx=60)
        self.ent_key = tk.Entry(self.root, width=15, **self.entry_style)
        self.ent_key.pack(pady=8)
        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack(pady=20)

       
        self.btn_enc = tk.Button(btn_frame, text="ENCRYPT", **self.btn_style)
        self.btn_enc.grid(row=0, column=0, padx=10, pady=10)

        self.btn_dec = tk.Button(btn_frame, text="DECRYPT", **self.btn_style)
        self.btn_dec.grid(row=0, column=1, padx=10, pady=10)

        self.btn_f_enc = tk.Button(btn_frame, text="SECURE FILE", **self.btn_style)
        self.btn_f_enc.grid(row=1, column=0, padx=10, pady=10)

        self.btn_f_dec = tk.Button(btn_frame, text="RESTORE FILE", **self.btn_style)
        self.btn_f_dec.grid(row=1, column=1, padx=10, pady=10)

       
        self.btn_exp = tk.Button(btn_frame, text="GENERATE QR TOKEN", bg="#0284c7", fg="white", 
                                 font=("Segoe UI", 10, "bold"), width=38, borderwidth=0)
        self.btn_exp.grid(row=2, column=0, columnspan=2, pady=1)
        self.lbl_output = tk.Label(self.root, text="SYSTEM READY", bg="#0f172a", fg="#94a3b8", 
                                   font=("Segoe UI", 9, "italic"))
        self.lbl_output.pack(pady=5)
       

    def show_image(self, path):   


        try:
          
            token_window = tk.Toplevel(self.root)
            token_window.title("SECURE TOKEN DISPLAY")
            token_window.configure(bg="#0f172a")
            token_window.geometry("300x350")
       
            img = Image.open(path)
            img = img.resize((250, 250), Image.LANCZOS)
            self.tk_photo = ImageTk.PhotoImage(img)               
            qr_messagebox = tk.Label(token_window, image=self.tk_photo, bg="#0f172a")
            qr_messagebox.image = self.tk_photo 
            qr_messagebox.pack(pady=20)
            
           
            close_btn = tk.Button(token_window, text="DISMISS TOKEN", 
                                  command=token_window.destroy,
                                  bg="#38bdf8")
        except Exception as e:
            print(f"CRITICAL UI ERROR:{e}")
