# 🎬 MD Video Maker / gaweVideo

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-WIP-orange)

## Bahasa Indonesia

**gaweVideo** adalah tool CLI Python untuk mengubah Markdown (`.md`) menjadi video tutorial coding 1080p siap upload YouTube.

### Fitur
- Parse Markdown menjadi scene (judul, paragraf, list, code, gambar)
- Highlight code block dengan tema (Monokai, Dracula, GitHub Dark, One Dark)
- Integrasi TTS natural via Microsoft Edge TTS
- Komposisi scene + transisi + audio (narasi & BGM)
- CLI cantik dengan Typer + Rich

### Instalasi
```bash
pip install -e .
```

Pastikan **FFmpeg** sudah terpasang.

### Quick Start
```bash
gawe-video generate examples/sample.md -o output.mp4 --theme dracula --voice id-ID-ArdiNeural
```

### Contoh Penggunaan
```bash
gawe-video generate examples/sample.md --preview
gawe-video generate examples/sample.md --bgm /path/music.mp3 --speed 1.1
gawe-video generate examples/sample.md --no-tts
```

### Web UI
Sekarang gaweVideo punya antarmuka web modern berbasis Streamlit:
- Sidebar settings (theme, voice, speed, resolution, FPS, BGM)
- Tab Upload & Generate, Preview Scenes, Templates, dan History
- Preview scene-by-scene dengan opsi re-order dan skip
- Session-based history untuk download ulang

![gaweVideo Web UI](https://github.com/user-attachments/assets/b2061f88-9bc8-485c-9473-3d4f546624db)

Jalankan Web UI:
```bash
gawe-video ui
```

Atau langsung via Streamlit:
```bash
streamlit run src/gawe_video/web_ui.py
```

> Catatan: preview/parsing bisa dijalankan tanpa FFmpeg, tetapi proses video production penuh tetap membutuhkan FFmpeg.

### Konfigurasi
Atur default pada `src/gawe_video/config.py`:
- Resolusi/FPS/bitrate video
- Tema code highlighting
- Voice dan rate TTS

### Sample Input & Output
Lihat `examples/sample.md` untuk contoh lengkap elemen markdown. Output final adalah MP4 H.264 + AAC dengan rasio 16:9.

### Contributing
1. Fork repository
2. Buat branch fitur
3. Tambahkan test
4. Kirim Pull Request

### License
MIT (`LICENSE`)

---

## English

**gaweVideo** is a Python CLI tool that converts Markdown (`.md`) into professional 1080p coding tutorial videos ready for YouTube.

### Features
- Markdown scene parsing (title, paragraph, list, code, image)
- Beautiful syntax-highlighted code blocks (Monokai, Dracula, GitHub Dark, One Dark)
- Natural narration with Microsoft Edge TTS
- Scene composition with transitions, narration, and BGM
- Friendly CLI using Typer + Rich

### Installation
```bash
pip install -e .
```

Make sure **FFmpeg** is installed.

### Quick Start
```bash
gawe-video generate examples/sample.md -o output.mp4 --theme monokai --voice en-US-GuyNeural
```

### Usage Examples
```bash
gawe-video generate examples/sample.md --preview
gawe-video generate examples/sample.md --bgm /path/music.mp3
gawe-video generate examples/sample.md --no-tts
```

### Web UI
gaweVideo now includes a modern Streamlit web interface with:
- Sidebar controls for theme, voice, speed, resolution, FPS, and BGM
- Upload & Generate, Scene Preview, Templates, and History tabs
- Scene-by-scene preview with reorder and skip controls
- Session-based generated video history for quick re-download

![gaweVideo Web UI](https://github.com/user-attachments/assets/b2061f88-9bc8-485c-9473-3d4f546624db)

Launch it with:
```bash
gawe-video ui
```

Or run Streamlit directly:
```bash
streamlit run src/gawe_video/web_ui.py
```

> Note: parsing/preview features can run without FFmpeg, but full production video workflows still require FFmpeg.

### Configuration
Edit defaults in `src/gawe_video/config.py`:
- Video resolution/FPS/bitrate
- Code themes and colors
- TTS voice and speed

### Sample Input & Expected Output
See `examples/sample.md` for a full markdown demo. The expected output is a YouTube-ready MP4 (H.264 video + AAC audio, 16:9).

### Contributing
1. Fork this repo
2. Create your feature branch
3. Add tests
4. Open a PR

### License
MIT (`LICENSE`)
