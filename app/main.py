from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))
try:
    from parser import parse_script
    from renderer import render_project
except:
    from app.parser import parse_script
    from app.renderer import render_project

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return (Path(__file__).parent.parent / "web" / "index.html").read_text(encoding="utf-8")

@app.post("/api/analyze")
async def analyze_script(file: UploadFile = File(...)):
    try:
        text = (await file.read()).decode("utf-8", errors="ignore")
        title = Path(file.filename).stem if file.filename else "Kich Ban"
        project = parse_script(text, title)
        images = render_project(project) # <-- Tao anh o day
        return {
            "status": "ok",
            "title": project.title,
            "scenes": len(project.scenes),
            "project": project.model_dump(),
            "images": images
        }
    except Exception as e:
        import traceback; traceback.print_exc()
        return {"status": "error", "message": str(e)}
