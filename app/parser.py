import re

def parse_script(text):
    """
    Phiên bản KHÔNG CẦN OpenAI - Chạy 100% local
    """
    scenes = []
    current_scene = {"title": "Cảnh 1", "dialogues": []}
    
    lines = text.strip().split('\n')
    
    scene_pattern = re.compile(r'^(Cảnh|Scene|CANH|SCENE)\s*(\d+)?\s*[-:]?\s*(.*)', re.IGNORECASE)
    dialogue_pattern = re.compile(r'^([^:]{1,20}):\s*(.+)$')

    scene_counter = 1

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        scene_match = scene_pattern.match(line)
        if scene_match:
            if current_scene["dialogues"]:
                scenes.append(current_scene)
            title = line if len(line) < 100 else f"Cảnh {scene_counter}"
            current_scene = {"title": title, "dialogues": []}
            scene_counter += 1
            continue
        
        dialogue_match = dialogue_pattern.match(line)
        if dialogue_match:
            character = dialogue_match.group(1).strip()
            dialogue = dialogue_match.group(2).strip()
            if len(character) <= 15:
                current_scene["dialogues"].append({
                    "character": character,
                    "text": dialogue
                })
        else:
            if current_scene["dialogues"]:
                current_scene["dialogues"][-1]["text"] += " " + line
            else:
                current_scene["dialogues"].append({
                    "character": "Người dẫn chuyện",
                    "text": line
                })

    if current_scene["dialogues"]:
        scenes.append(current_scene)
    
    if not scenes:
        all_dialogues = []
        for line in lines:
            if line.strip():
                dm = dialogue_pattern.match(line.strip())
                if dm and len(dm.group(1).strip()) <= 15:
                    all_dialogues.append({"character": dm.group(1).strip(), "text": dm.group(2).strip()})
                else:
                    all_dialogues.append({"character": "Người dẫn chuyện", "text": line.strip()})
        scenes = [{"title": "Cảnh 1", "dialogues": all_dialogues}]
        
    return scenes
