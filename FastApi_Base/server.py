from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import socket

app = FastAPI()


class OptionRequest(BaseModel):
    option: int


app.mount("/static", StaticFiles(directory="static"), name="static")


def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return print(s.getsockname()[0])


@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")


@app.get("/page/{page_number}")
async def get_page(page_number: int):
    if page_number in [1, 2, 3]:
        return FileResponse(f"static/page{page_number}.html")
    return {"error": "Page not found"}


@app.post("/api/select")
async def handle_selection(request: OptionRequest):
    return {"redirect_url": f"/page/{request.option}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
