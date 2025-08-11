# ui_utils.py

import tkinter as tk
from PIL import ImageTk
import qrcode
import threading

def show_qr_async(ip, port):
    def run():
        show_qr(ip, port)
    threading.Thread(target=run, daemon=True).start()

def show_qr(ip, port):
    url = f"http://{ip}:{port}/index.html"
    qr_img = qrcode.make(url)

    root = tk.Tk()
    root.title("Server QR-Code") # window title

    qr_img = qr_img.resize((300, 300))
    tk_img = ImageTk.PhotoImage(qr_img)

    label = tk.Label(root, image=tk_img) # label for qr code
    label.pack(padx=20, pady=20)

    text = tk.Label(root, text=url, font=("Arial", 12)) # label for server url
    text.pack(pady=(0, 20))

    root.mainloop()
