import tkinter as tk
from PIL import Image, ImageTk


class CipherView:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Local Vault")
        self.root.geometry("550x850")
        self.root.configure(bg="#0f172a")
        self.label_style = {"bg": "#0f172a", "fg": "#38bdf8", "font": ("Segoe UI", 10, "bold")}
        self.entry_style = {"bg": "#1e293b", "fg": "#f1f5f9", "insertbackground": "#38bdf8", "font": ("Segoe UI", 11), "borderwidth": 0, "highlightthickness": 1, "highlightbackground": "#334155"}
        self.btn_style = {"bg": "#0ea5e9", "fg": "#ffffff", "font": ("Segoe UI", 10, "bold"), "activebackground": "#38bdf8", "borderwidth": 0, "cursor": "hand2", "width": 18}
        tk.Label(root, text="SECURE LOCAL VAULT", bg="#0f172a", fg="#f1f5f9", font=("Segoe UI", 14, "bold")).pack(pady=20)
        tk.Label(root, text="TEXT OR FILE CONTENT", **self.label_style).pack(anchor="w", padx=60)
        self.ent_msg = tk.Entry(root, width=40, **self.entry_style)
        self.ent_msg.pack(pady=8)
        tk.Label(root, text="ENCRYPTION KEY", **self.label_style).pack(anchor="w", padx=60)
        self.ent_key = tk.Entry(root, width=30, show="*", **self.entry_style)
        self.ent_key.pack(pady=8)
        frame = tk.Frame(root, bg="#0f172a")
        frame.pack(pady=20)
        self.btn_enc = tk.Button(frame, text="ENCRYPT TEXT", **self.btn_style)
        self.btn_enc.grid(row=0, column=0, padx=10, pady=10)
        self.btn_dec = tk.Button(frame, text="DECRYPT TEXT", **self.btn_style)
        self.btn_dec.grid(row=0, column=1, padx=10, pady=10)
        self.btn_f_enc = tk.Button(frame, text="ENCRYPT FILE", **self.btn_style)
        self.btn_f_enc.grid(row=1, column=0, padx=10, pady=10)
        self.btn_f_dec = tk.Button(frame, text="RESTORE FILE", **self.btn_style)
        self.btn_f_dec.grid(row=1, column=1, padx=10, pady=10)
        self.btn_exp = tk.Button(frame, text="GENERATE QR TOKEN", bg="#0284c7", fg="white", font=("Segoe UI", 10, "bold"), width=38, borderwidth=0)
        self.btn_exp.grid(row=2, column=0, columnspan=2, pady=1)
        self.lbl_output = tk.Label(root, text="Ready", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 9, "italic"))
        self.lbl_output.pack(pady=5)

    def show_image(self, path):
        token_window = tk.Toplevel(self.root)
        token_window.title("QR Token")
        token_window.configure(bg="#0f172a")
        img = Image.open(path).resize((250, 250), Image.Resampling.LANCZOS)
        self.tk_photo = ImageTk.PhotoImage(img)
        tk.Label(token_window, image=self.tk_photo, bg="#0f172a").pack(pady=20)
        tk.Button(token_window, text="Close", command=token_window.destroy, bg="#38bdf8").pack(pady=10)
