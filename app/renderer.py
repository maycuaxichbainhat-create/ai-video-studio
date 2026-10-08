import urllib.parse

def get_image_url(prompt, seed=42):
    # Dùng Pollinations - tạo ảnh miễn phí, không cần key
    safe_prompt = urllib.parse.quote(f"{prompt}, 3d cinematic, Vietnam 2050, ultra detailed, 8k")
    return f"https://image.pollinations.ai/prompt/{safe_prompt}?seed={seed}&width=1280&height=720&nologo=true"

def render_project(project, output_path=None):
    images = []
    for scene in project.scenes:
        # Lay cau thoai dau tien lam prompt anh
        text = scene.dialogue[0].text if scene.dialogue else scene.background
        prompt = f"{scene.background}, {text}"
        url = get_image_url(prompt, seed=scene.number*10)
        images.append({"scene": scene.number, "prompt": prompt, "image_url": url})
    return images
