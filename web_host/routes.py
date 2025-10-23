import os
from pathlib import Path
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
import docker

IMAGE = os.getenv("SHERLOCK_IMAGE", "sherlock/sherlock:latest")
DATA_DIR = Path(__file__).parent.joinpath("..", "data").resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
client = docker.from_env()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/health")
async def health():
    try:
        client.ping()
        return {"status": "ok", "image": IMAGE}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@router.post("/run", response_class=PlainTextResponse)
async def run(username: str = Form(...), format: str = Form("csv")):
    username = username.strip()
    if not username:
        return PlainTextResponse("Username vide.", status_code=400)

    export_flag = "--csv" if format == "csv" else "--json"
    volumes = {str(DATA_DIR): {"bind": "/data", "mode": "rw"}}
    safe_user = username.replace("/", "_").replace("\\", "_").strip()
    ext = "csv" if format == "csv" else "json"
    out_file = f"/data/{safe_user}.{ext}"
    cmd = f"{safe_user} -o {out_file} {export_flag}" 

    try:
        logs = client.containers.run(
            IMAGE,
            command=cmd,
            volumes=volumes,
            remove=True,
            tty=False,
            stdin_open=False
        )
        return logs.decode("utf-8", errors="ignore")
    except docker.errors.ImageNotFound:
        return PlainTextResponse(
            f"Image introuvable: {IMAGE}. Faites `docker pull {IMAGE}` ou définissez SHERLOCK_IMAGE sur votre image buildée.",
            status_code=500
        )
    except docker.errors.APIError as e:
        return PlainTextResponse(f"Erreur Docker API: {e.explanation}", status_code=500)
    except Exception as e:
        return PlainTextResponse(f"Erreur: {e}", status_code=500)