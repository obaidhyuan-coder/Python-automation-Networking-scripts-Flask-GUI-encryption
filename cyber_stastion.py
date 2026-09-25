import tkinter as tk
from View import CipherView
from Controller import CipherController
from Login_View import LoginWindow
from AdvancedCipher import AdvancedCipher

if __name__ == "__main__":

 login_root = tk.Tk()
 login_app = LoginWindow(login_root)
 login_root.mainloop()

 if login_app.is_authenticated:
  
  root = tk.Tk()
  view = CipherView(root)
  engine = AdvancedCipher(key="some_key",agent="Agent_007")
  controller =   CipherController(view,engine)
  root.mainloop()

