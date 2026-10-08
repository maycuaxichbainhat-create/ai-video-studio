import urllib.parse

def get_image_url(prompt_vi, canh_num):
    # Tao anh AI mien phi - hieu tieng Viet
    prompt_en = f"{prompt_vi}, Vietnamese village 2050, futuristic rice field, 3d cinematic, ultra detailed, 8k, vibrant"
    safe = urllib.parse.quote(prompt_en[:800])
    # Moi canh 1 seed khac nhau cho anh khac nhau
    return f"https://image.pollinations.ai/prompt/{safe}?seed={canh_num*77}&width=1024&height=576&nologo=true&model=flux"

def render_project(project):
    result = []
    for scene in project.scenes:
        # Lay mo ta canh lam prompt
        bg = scene.background or f"Canh {scene.number}"
        # Cat bo thoi gian 0:30-1:30 de lam prompt sach
        bg_clean = bg.split('Lời dẫn:')[-1][:200]
        url = get_image_url(bg_clean, scene.number)
        result.append({
            "number": scene.number,
            "background": scene.background,
            "image_url": url,
            "dialogue": [d.text for d in scene.dialogue[:2]]
        })
    return result

def create_video_from_images(image_urls, output_path):
    # Tao video tu anh - se lam o frontend truoc
    return output_path
