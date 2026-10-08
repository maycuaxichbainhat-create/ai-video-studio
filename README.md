# AI Video Studio V1

**TXT → Scene Parser → Multi-character project → Render MP4 → Download**

Đây là bộ khung mã nguồn mở để phát triển một tool dựng video từ kịch bản. V1 ưu tiên:
- Xuất MP4 và tải video trực tiếp từ giao diện.
- Nhiều nhân vật trong một cảnh.
- Lời thoại riêng cho từng nhân vật.
- Mỗi nhân vật có thể gán voice ID riêng.
- Bối cảnh, nhạc và SFX theo từng cảnh.
- Kiến trúc adapter/pipeline để sau này gắn Blender, TTS, AI image/video hoặc dịch vụ khác.

> Quan trọng: GitHub chỉ lưu mã nguồn. Nó không tự biến code thành hệ thống AI tạo 3D. Để có nhân vật 3D chuyển động/lip-sync thực tế cần gắn engine 3D/TTS/AI vào các adapter. Renderer V1 hiện tạo MP4 hợp lệ bằng FFmpeg để kiểm tra toàn bộ pipeline.

## 1. Cài trên Windows

Cần:
1. Git
2. Python 3.11+
3. FFmpeg

Kiểm tra:
```powershell
git --version
python --version
ffmpeg -version
```

## 2. Chạy local

Giải nén project:

```powershell
cd ai-video-studio-v1
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Mở:

```text
http://127.0.0.1:8000
```

Hoặc chạy:

```text
run_windows.bat
```

## 3. Test bằng kịch bản mẫu

Chọn `sample_script.txt`.

Tool sẽ phát hiện:
- 3 cảnh
- Kai
- Mira
- Robot chiến đấu
- lời thoại của từng nhân vật
- bối cảnh
- nhạc
- SFX

Sau đó bấm **Dựng video MP4** và chọn **TẢI VIDEO MP4**.

## 4. Đưa code lên GitHub

Trên GitHub tạo repository mới, ví dụ:

`ai-video-studio`

Nếu dùng GitHub web, khi nhập code local vào repository mới nên tạo repository trống, không cần README/.gitignore/license vì project local đã có các file đó.

Trong thư mục project:

```powershell
git init
git add .
git commit -m "Initial AI Video Studio V1"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-video-studio.git
git push -u origin main
```

Thay `YOUR_USERNAME` bằng username GitHub của bạn.

## 5. Cập nhật code về sau

```powershell
git add .
git commit -m "Update video pipeline"
git push
```

## 6. Cấu trúc

```text
ai-video-studio/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── parser.py
│   └── renderer.py
├── assets/
│   ├── characters/
│   ├── backgrounds/
│   └── audio/
├── projects/
├── renders/
├── web/
│   └── index.html
├── .env.example
├── .gitignore
├── requirements.txt
├── run_windows.bat
└── sample_script.txt
```

## 7. Roadmap V2

V2 nên bổ sung theo đúng mục tiêu sản xuất video:
1. Character Library: nhiều mẫu nhân vật 3D.
2. Character Lock: giữ đúng khuôn mặt/trang phục giữa các cảnh.
3. Voice Library: mỗi nhân vật một giọng.
4. TTS: tạo file WAV cho từng câu thoại.
5. Lip-sync.
6. Blender adapter: animation/camera/render 3D.
7. Background Library.
8. AI image/video adapter.
9. Subtitle.
10. Timeline editor.
11. Batch render.
12. Resume render khi một cảnh lỗi.
13. MP4 1080p/4K.
14. Nút Download Video.
15. Project export/import.

## 8. Nguyên tắc kiến trúc

Không khóa hệ thống vào một engine:

```text
Script
  ↓
Parser
  ↓
Scene JSON
  ↓
Character Adapter ──→ Blender / 3D engine
  ↓
Voice Adapter ──────→ TTS engine
  ↓
Background Adapter ─→ images/video/3D
  ↓
Audio Mixer
  ↓
Renderer
  ↓
FFmpeg
  ↓
MP4
```

Nhờ vậy có thể thay từng engine mà không phải viết lại toàn bộ ứng dụng.
