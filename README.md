# Face Giffer - Time-lapse GIF Generator

Create an animated GIF from a series of portrait selfies with automatic face alignment and brightness normalization.

## Features

- ✅ Converts HEIC (Apple) images to JPEG
- ✅ Sorts images chronologically using EXIF metadata (with fallback to file modification time)
- ✅ Detects and aligns faces using dlib's 68-point facial landmarks
- ✅ Normalizes brightness/contrast across all frames using CLAHE
- ✅ Generates smooth animated GIF output

## Prerequisites

- Python 3.10+
- `uv` (installed via `mise`)
- `cmake` (for building dlib)

## Setup

### 1. Install uv via mise

```bash
/home/karolis/.local/bin/mise trust
/home/karolis/.local/bin/mise install uv
```

### 2. Install Dependencies

```bash
uv sync
```

This will create a virtual environment (`.venv`) and install all required packages:
- opencv-python
- numpy
- pillow
- pillow-heif
- imageio
- dlib
- gdown

### 3. Download dlib Face Landmark Model

The script requires `shape_predictor_68_face_landmarks.dat` (~100MB).

**Option A: Manual Download**
- Download from: https://sourceforge.net/projects/dclib/files/dlib/v19.24/shape_predictor_68_face_landmarks.dat.bz2
- Extract the `.bz2` file
- Place the `.dat` file in the project root directory

**Option B: Automatic Download**
```bash
python -c "import gdown; gdown.download('https://drive.google.com/uc?id=1nJf1_ByRy8j4_sPl3MEFaFjYDvVOA44F', 'shape_predictor_68_face_landmarks.dat.bz2'); import bz2; bz2.open('shape_predictor_68_face_landmarks.dat.bz2').read()" > shape_predictor_68_face_landmarks.dat
```

## Usage

### 1. Prepare Input Images

Place all your selfie images in the `input/` directory:
- Supported formats: HEIC, JPG, PNG
- The directory is ignored by git (`.gitignore`)

```bash
input/
├── IMG_0001.HEIC
├── IMG_0002.HEIC
├── photo_2023.jpg
└── ...
```

### 2. Run the Script

```bash
source .venv/bin/activate
python face_giffer.py
```

Or using uv directly:
```bash
uv run face_giffer.py
```

### 3. Output

The script creates:
- `processed/` - Converted JPEG images (intermediate stage)
- `output/timelapse.gif` - Final animated GIF
- Frame-by-frame alignments saved for inspection

## Project Structure

```
face-giffer/
├── face_giffer.py              # Main orchestration script
├── preprocessing.py            # HEIC conversion, sorting, EXIF extraction
├── face_alignment.py           # Face detection and alignment using dlib
├── normalization.py            # Brightness normalization and GIF creation
├── pyproject.toml              # Project configuration (uv)
├── mise.toml                   # Tool configuration
├── input/                      # Input images (git ignored)
├── processed/                  # Converted/aligned frames (intermediate)
├── output/                     # Final GIF output
└── README.md                   # This file
```

## Configuration

Edit parameters in `face_giffer.py`:

```python
giffer = FaceGiffer()
# Customize directories if needed:
# giffer = FaceGiffer(input_dir="my_photos", output_dir="results")

# Customize GIF settings:
# giffer.create_gif(normalized_images, fps=15, output_path="custom.gif")
```

In `face_alignment.py`, adjust face alignment parameters:
- `output_size`: Dimensions of aligned faces (default: 512×768 for portrait)
- `eye_y_ratio`: Vertical position of eyes (0.3 = 30% from top)
- `eye_x_ratio_left/right`: Horizontal positions of eyes

## Troubleshooting

### ImportError: dlib not found
- Ensure `uv sync` completed successfully
- CMake must be installed: `brew install cmake`

### No faces detected
- Ensure images contain clear facial features
- Try lower resolution or different lighting

### EXIF data not found
- The script falls back to file modification time automatically
- Rename files with dates for better sorting (e.g., `IMG_20230101.jpg`)

### Out of memory
- Process images in batches by editing `preprocess_images()` function
- Reduce `output_size` in face alignment

## Performance

- Processing time depends on image count and resolution
- ~10-30 seconds per image for face alignment on modern hardware
- GIF generation adds ~1-2 seconds per frame

## License

MIT

## References

- dlib: http://dlib.net/
- OpenCV: https://opencv.org/
- Pillow: https://python-pillow.org/
