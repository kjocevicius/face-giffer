# Face Giffer

Create an animated time-lapse GIF from portrait selfies with automatic face alignment and brightness normalization.

## Features

- **HEIC Conversion** - Converts Apple HEIC images to JPEG
- **Chronological Sorting** - Sorts images by EXIF date (with filename/mtime fallback)
- **Face Alignment** - Detects and aligns faces using dlib's 68-point landmarks
- **Brightness Normalization** - Applies CLAHE for consistent tones across frames
- **GIF Generation** - Creates smooth animated GIF output

## Quick Start

```bash
# Install dependencies
uv sync

# Download dlib face model (~100MB)
uv run python -m src.download_model

# Place images in input/ folder
mkdir -p input
# Copy your selfies to input/

# Run
uv run python main.py
```

Output: `output/timelapse.gif`

## Requirements

- Python 3.10-3.12
- uv (via mise)
- cmake (for building dlib)

## Configuration

Edit [src/settings.py](src/settings.py) to customize:

```python
OUTPUT_SIZE = (1024, 1024)  # Square output
GIF_FPS = 10               # Frames per second
EYE_Y_RATIO = 0.35         # Eye vertical position
```

## Project Structure

```
face-giffer/
├── main.py                 # Entry point
├── src/
│   ├── settings.py         # Configuration
│   ├── preprocessing.py    # HEIC conversion, sorting
│   ├── face_alignment.py   # Face detection & alignment
│   ├── normalization.py    # CLAHE & GIF creation
│   └── download_model.py   # Model download utility
├── input/                  # Source images (gitignored)
├── processed/              # Converted images (gitignored)
└── output/                 # Final GIF (gitignored)
```

## Supported Formats

- HEIC (Apple)
- JPEG/JPG
- PNG

## License

MIT
