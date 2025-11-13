import requests
import webbrowser
import tkinter as tk
from tkinter import messagebox


def connect_to_server(server_ip):
    try:
        url = f"http://{server_ip}:8000"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            webbrowser.open(url)
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False


def start_client():

    def on_connect():
        ip = ip_entry.get().strip()
        if not ip:
            messagebox.showerror("Ошибка", "Введите IP адрес сервера")
            return

        status_label.config(text="Поиск сервера...")
        root.update()

        if connect_to_server(ip):
            status_label.config(text=f"Успешно! Открываю {ip}")
        else:
            status_label.config(text="Ошибка подключения")
            messagebox.showerror("Ошибка", "Не удалось подключиться к серверу")

    root = tk.Tk()
    root.title("Клиент")
    root.geometry("300x150")

    tk.Label(root, text="IP адрес сервера:").pack(pady=10)

    ip_entry = tk.Entry(root, width=20)
    ip_entry.pack(pady=5)

    connect_btn = tk.Button(root, text="Подключиться", command=on_connect)
    connect_btn.pack(pady=10)

    status_label = tk.Label(root, text="")
    status_label.pack()

    root.mainloop()


if __name__ == "__main__":
    start_client()
