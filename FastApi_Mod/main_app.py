import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import sys


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FastAPI Launcher")
        self.root.geometry("400x200")
        self.server_process = None
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Выберите что запустить:",
                               font=("Arial", 14))
        title_label.pack(pady=20)

        selection_frame = tk.Frame(self.root)
        selection_frame.pack(pady=10)

        self.server_var = tk.BooleanVar()
        self.client_var = tk.BooleanVar()

        server_check = tk.Checkbutton(selection_frame, text="Запустить Сервер",
                                      variable=self.server_var,
                                      command=self.on_server_toggle)
        server_check.pack(anchor="w")

        client_check = tk.Checkbutton(selection_frame, text="Запустить Клиент",
                                      variable=self.client_var)
        client_check.pack(anchor="w")

        self.ip_frame = tk.Frame(self.root)
        self.ip_label = tk.Label(self.ip_frame, text="IP сервера:")
        self.ip_entry = tk.Entry(self.ip_frame, width=20)
        self.ip_frame.pack(pady=5)
        self.ip_frame.pack_forget()  # Скрываем по умолчанию

        self.start_btn = tk.Button(self.root, text="Запуск",
                                   command=self.start_apps,
                                   bg="green", fg="white", font=("Arial", 12))
        self.start_btn.pack(pady=20)
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack()

    def on_server_toggle(self):
        if self.client_var.get():
            self.ip_label.pack(side="left")
            self.ip_entry.pack(side="left")
            self.ip_frame.pack()
        else:
            self.ip_frame.pack_forget()

    def start_apps(self):
        if not self.server_var.get() and not self.client_var.get():
            messagebox.showwarning("Внимание", "Выберите хотя бы один вариант")
            return

        self.start_btn.config(state="disabled")
        self.status_label.config(text="Запуск...")

        if self.server_var.get():
            server_thread = threading.Thread(target=self.start_server)
            server_thread.daemon = True
            server_thread.start()

        if self.client_var.get():
            client_thread = threading.Thread(target=self.start_client)
            client_thread.daemon = True
            client_thread.start()

    def start_server(self):
        try:
            self.status_label.config(text="Запуск сервера...")
            self.server_process = subprocess.Popen(
                [sys.executable, "server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.status_label.config(text="Сервер запущен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка запуска сервера: {e}")

    def start_client(self):
        try:
            self.status_label.config(text="Запуск клиента...")
            subprocess.Popen([sys.executable, "client.py"])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка запуска клиента: {e}")

    def on_closing(self):
        if self.server_process:
            self.server_process.terminate()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
