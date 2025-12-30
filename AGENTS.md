# AGENTS.md

Instructions for AI coding agents working on this repository.

## Project Overview

Face Giffer is a Python tool that creates time-lapse GIFs from portrait selfies with automatic face alignment.

## Tech Stack

- **Python 3.10-3.12** (managed via uv)
- **uv** - Package manager (installed via mise)
- **dlib** - Face detection and 68-point landmark prediction
- **OpenCV** - Image processing and affine transformations
- **Pillow + pillow-heif** - Image loading and HEIC conversion
- **imageio** - GIF creation

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point, orchestrates the workflow |
| `src/settings.py` | All configurable constants |
| `src/preprocessing.py` | HEIC→JPEG conversion, EXIF extraction, chronological sorting |
| `src/face_alignment.py` | Face detection, landmark extraction, affine transformation |
| `src/normalization.py` | CLAHE brightness normalization, GIF compilation |

## Commands

```bash
# Install dependencies
uv sync

# Run the tool
uv run python main.py

# Download dlib model
uv run python -m src.download_model
```

## Architecture Notes

1. **Preprocessing**: Converts HEIC to JPEG (skips if already done), extracts EXIF dates from originals before conversion, sorts chronologically
2. **Face Alignment**: Uses dlib's frontal face detector + 68-point shape predictor, applies affine transformation to align eyes to fixed coordinates
3. **Normalization**: CLAHE on LAB color space L-channel for consistent brightness
4. **GIF Creation**: imageio with configurable FPS

## Configuration

All settings are in `src/settings.py`:
- `OUTPUT_SIZE` - Output dimensions (default: 1024x1024)
- `EYE_Y_RATIO` / `EYE_X_RATIO_*` - Face positioning
- `GIF_FPS` - Animation speed
- `SKIP_EXISTING` - Skip already-processed files

## Testing Changes

After making changes, run:
```bash
uv run python main.py
```

Check `output/timelapse.gif` for results.

## Common Issues

- **dlib build fails**: Ensure cmake is installed (`brew install cmake`)
- **No face detected**: Image may be too dark, face occluded, or at unusual angle
- **Wrong sorting**: Check EXIF data in source images
