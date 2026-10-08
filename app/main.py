from pathlib import Path
import json, uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from .parser import parse_script
from .renderer import render_project

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
PROJECTS = ROOT / "projects"

app = FastAPI(title="AI Video Studio V1")

@app.get("/", response_class=HTMLResponse)
def home():
    return (WEB / "index.html").read_text(encoding="utf-8")

@app.post("/api/parse")
async def parse(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(400, "V1 nhận file TXT.")
    text = (await file.read()).decode("utf-8-sig")
    project = parse_script(text, Path(file.filename).stem)
    pid = uuid.uuid4().hex
    path = PROJECTS / f"{pid}.json"
    path.write_text(project.model_dump_json(indent=2), encoding="utf-8")
    return {"project_id": pid, "project": project.model_dump()}

@app.post("/api/render/{project_id}")
def render(project_id: str):
    path = PROJECTS / f"{project_id}.json"
    if not path.exists():
        raise HTTPException(404, "Không tìm thấy project.")
    from .models import Project
    project = Project.model_validate_json(path.read_text(encoding="utf-8"))
    out = render_project(project)
    return {"download": f"/api/download/{out.name}"}

@app.get("/api/download/{filename}")
def download(filename: str):
    path = ROOT / "renders" / filename
    if not path.exists():
        raise HTTPException(404, "Không tìm thấy video.")
    return FileResponse(path, media_type="video/mp4", filename=filename)
