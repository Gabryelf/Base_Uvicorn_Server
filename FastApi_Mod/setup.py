from cx_Freeze import setup, Executable
import sys

# Зависимости
build_exe_options = {
    "packages": ["fastapi", "uvicorn", "pydantic", "tkinter", "requests"],
    "includes": ["static"],
    "include_files": [
        ("static/", "static/"),
    ],
}

# Настройки для exe
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="FastAPI Launcher",
    version="1.0",
    description="FastAPI Server and Client Launcher",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("main_app.py", base=base, target_name="FastAPI_Launcher.exe"),
        Executable("server.py", base=None, target_name="server.exe"),
        Executable("client.py", base=base, target_name="client.exe")
    ]
)
