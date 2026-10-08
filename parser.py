import re
from .models import Project, Scene, Character, Dialogue

def parse_script(text: str, title: str = "Untitled Project") -> Project:
    blocks = re.split(r"(?im)^\s*CẢNH\s+(\d+)\s*$", text)
    scenes = []
    # blocks = preamble, number, content, number, content...
    for i in range(1, len(blocks), 2):
        number = int(blocks[i])
        content = blocks[i + 1]
        background = ""
        chars = []
        dialogues = []
        music = None
        sfx = []
        for raw in content.splitlines():
            line = raw.strip()
            if not line:
                continue
            m = re.match(r"(?i)^BỐI CẢNH\s*:\s*(.+)$", line)
            if m:
                background = m.group(1).strip()
                continue
            m = re.match(r"(?i)^NHẠC\s*:\s*(.+)$", line)
            if m:
                music = m.group(1).strip()
                continue
            m = re.match(r"(?i)^SFX\s*:\s*(.+)$", line)
            if m:
                sfx.extend([x.strip() for x in m.group(1).split(",")])
                continue
            m = re.match(r"^([^:]{1,60})\s*:\s*(.+)$", line)
            if m:
                name, speech = m.group(1).strip(), m.group(2).strip()
                if name.upper() not in {"BỐI CẢNH", "NHẠC", "SFX"}:
                    dialogues.append(Dialogue(character=name, text=speech))
                    if not any(c.name == name for c in chars):
                        chars.append(Character(name=name))
        duration = max(4.0, sum(max(2.0, len(d.text) / 12) for d in dialogues))
        scenes.append(Scene(number=number, background=background,
                            characters=chars, dialogue=dialogues,
                            music=music, sfx=sfx, duration=duration))
    return Project(title=title, scenes=scenes)
