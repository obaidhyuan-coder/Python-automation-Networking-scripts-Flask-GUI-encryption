import tkinter as tk

from Login_View import LoginWindow
from AdvancedCipher import AdvancedCipher
from Controller import CipherController
from View import CipherView


def main():
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()

    if not login_app.is_authenticated:
        return

    root = tk.Tk()
    view = CipherView(root)
    engine = AdvancedCipher(key="demo_key", agent="local-demo")
    CipherController(view, engine)
    root.mainloop()


if __name__ == "__main__":
    main()
