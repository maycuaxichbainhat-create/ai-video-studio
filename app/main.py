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
    html_file = Path(__file__).parent.parent / "web" / "index.html"
    return html_file.read_text(encoding="utf-8")

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        text = (await file.read()).decode("utf-8", errors="ignore")
        title = Path(file.filename).stem if file.filename else "KichBan"
        project = parse_script(text, title)
        images = render_project(project)
        return {"status":"ok","title":project.title,"scenes":len(project.scenes),"images":images,"project":project.model_dump()}
    except Exception as e:
        import traceback; traceback.print_exc()
        return {"status":"error","message":str(e)}

@app.get("/api/health")
async def health():
    return {"status":"ok"}
