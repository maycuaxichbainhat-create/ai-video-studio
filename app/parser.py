import re
from typing import List
from.models import Project, Scene, Character, Dialogue

def parse_script(text: str, title: str = "Kich Ban") -> Project:
    text = text.strip()
    if not text:
        return Project(title=title, scenes=[])

    pattern = r'(?:CẢNH|Canh|CANH|Scene|SCENE)\s*(\d+)[\s:\-]*([^\n]*)'
    matches = list(re.finditer(pattern, text))

    scenes: List[Scene] = []

    if len(matches) >= 1:
        # CO DANH DAU CANH -> Lay het, khong gioi han
        for i, m in enumerate(matches):
            canh_num = int(m.group(1))
            start = m.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            content = text[start:end].strip()
            bg = m.group(2).strip() or content[:200] or f"Canh {canh_num}"

            dialogues = []
            for line in content.split('\n'):
                if ':' in line and len(line) < 300:
                    name, txt = line.split(':', 1)
                    if len(name.strip()) < 40 and len(txt.strip()) > 2:
                        dialogues.append(Dialogue(character=name.strip(), text=txt.strip()))

            if not dialogues:
                dialogues = [Dialogue(character="Dan lang", text=content[:400] or bg)]

            scenes.append(Scene(
                number=canh_num,
                background=bg[:400],
                characters=[Character(name="Nhan vat", style="3d_cinematic", asset=None, voice="default")],
                dialogue=dialogues
            ))
    else:
        # KHONG CO DANH DAU -> Moi dong la 1 canh, lay het
        lines = [p.strip() for p in text.replace('\r','').split('\n') if p.strip()]
        # Gom 2-3 dong thanh 1 canh neu dong ngan
        buffer = ""
        idx = 1
        for line in lines:
            buffer += " " + line
            if len(buffer) > 100: # Du 100 ky tu thi tao 1 canh
                scenes.append(Scene(
                    number=idx,
                    background=buffer[:400],
                    characters=[Character(name="Nhan vat", style="3d_cinematic", asset=None, voice="default")],
                    dialogue=[Dialogue(character="Nguoi ke", text=buffer[:400])]
                ))
                idx += 1
                buffer = ""
        if buffer.strip():
            scenes.append(Scene(number=idx, background=buffer[:400], characters=[Character(name="Nhan vat", style="3d_cinematic", asset=None, voice="default")], dialogue=[Dialogue(character="Nguoi ke", text=buffer[:400])]))

    scenes.sort(key=lambda s: s.number)
    return Project(title=title, scenes=scenes)
