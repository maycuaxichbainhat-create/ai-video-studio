import os
import uuid
from pathlib import Path

def render_project(du_an, output_path=None):
    # Ban nay KHONG CAN ffmpeg, KHONG CAN OpenAI - chi de test cho chay
    print(f"Render: {du_an.title} - {len(du_an.scenes)} canh")
    # Tra ve file mau
    base = Path(__file__).resolve().parent.parent / "render"
    base.mkdir(exist_ok=True)
    out = base / f"{uuid.uuid4().hex[:8]}.mp4"
    out.touch()
    return out
