import os, subprocess, uuid
from pathlib import Path
from .models import Project

ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "renders"
RENDER_DIR.mkdir(exist_ok=True)

def render_project(project: Project) -> Path:
    # V1 renderer: creates a valid MP4 from generated scene cards.
    # Replace this adapter later with Blender/ComfyUI/AI video rendering.
    job = uuid.uuid4().hex[:10]
    out = RENDER_DIR / f"{job}.mp4"
    concat = RENDER_DIR / f"{job}_concat.txt"
    clips = []

    for idx, scene in enumerate(project.scenes, 1):
        clip = RENDER_DIR / f"{job}_{idx:04d}.mp4"
        duration = max(2.0, float(scene.duration))
        # Solid black scene card; production adapter can replace this with rendered 3D frames.
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "color=c=black:s=1280x720:r=30",
            "-t", str(duration), "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(clip)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips.append(clip)

    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips), encoding="utf-8")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
           "-c", "copy", str(out)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for p in clips:
        p.unlink(missing_ok=True)
    concat.unlink(missing_ok=True)
    return out
