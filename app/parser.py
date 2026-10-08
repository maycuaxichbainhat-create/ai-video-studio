from.models import Project, Scene, Character, Dialogue
import re

def parse_script(text: str, title: str = "Kich Ban"):
    # Tach thanh cac canh nho
    # Neu co chu CANH thi tach theo CANH, khong thi tach theo doan van
    text = text.strip()
    if not text:
        text = "Xin chao. Day la canh mau."

    # Tach theo dong trong
    raw_scenes = re.split(r'\n\s*\n', text)
    # Loai bo doan qua ngan
    raw_scenes = [s.strip() for s in raw_scenes if len(s.strip()) > 5]

    if not raw_scenes:
        raw_scenes = [text]

    scenes = []
    for i, scene_text in enumerate(raw_scenes[:10], 1): # toi da 10 canh
        # Lay 2-3 cau dau lam thoai
        sentences = re.split(r'[.!?]+', scene_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        dialogues = []
        for sent in sentences[:3]:
            if len(sent) > 3:
                dialogues.append(Dialogue(character=f"Nhan vat {i}", text=sent, voice="default"))

        if not dialogues:
            dialogues = [Dialogue(character="Nguoi dan", text=scene_text[:200], voice="default")]

        # Nhan vat mac dinh
        char = Character(name=f"Nhan vat {i}", style="3d_cinematic", voice="default")

        scene = Scene(
            number=i,
            background=f"Canh {i} - {title}",
            characters=[char],
            dialogue=dialogues,
            duration=5.0
        )
        scenes.append(scene)

    project = Project(title=title, scenes=scenes)
    return project
