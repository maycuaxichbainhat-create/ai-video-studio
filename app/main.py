from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pathlib import Path
import sys

# Fix import cho Render
sys.path.append(str(Path(__file__).parent))

try:
    from parser import parse_script
except:
    from app.parser import parse_script

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    try:
        html_path = Path(__file__).parent.parent / "web" / "index.html"
        return html_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"<h1>AI Video Studio - Loi doc file: {e}</h1>"

@app.post("/api/analyze")
async def analyze_script(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("utf-8", errors="ignore")
        if not text.strip():
            return {"status": "error", "message": "File rong!"}
        
        title = Path(file.filename).stem if file.filename else "Kich Ban"
        project = parse_script(text, title)
        
        return {
            "status": "ok",
            "title": project.title,
            "scenes": len(project.scenes),
            "project": project.model_dump()
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": f"Loi server: {str(e)}"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}
