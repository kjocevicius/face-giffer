"""Configuration settings for Face Giffer."""

from pathlib import Path

# ============================================================================
# DIRECTORIES
# ============================================================================
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
PROCESSED_DIR = Path("processed")

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================
# Output dimensions (width, height) - square format for better face visibility
OUTPUT_SIZE = (1024, 1024)

# ============================================================================
# FACE ALIGNMENT SETTINGS
# ============================================================================
# Vertical position of eyes (0.0 = top, 1.0 = bottom)
# 0.35 places eyes slightly above center for good framing
EYE_Y_RATIO = 0.35

# Horizontal positions of eyes (0.0 = left, 1.0 = right)
EYE_X_RATIO_LEFT = 0.35
EYE_X_RATIO_RIGHT = 0.65

# ============================================================================
# DLIB MODEL
# ============================================================================
MODEL_PATH = Path("shape_predictor_68_face_landmarks.dat")
MODEL_URL = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"

# ============================================================================
# GIF SETTINGS
# ============================================================================
GIF_FPS = 10
GIF_LOOP = 0  # 0 = infinite loop

# ============================================================================
# NORMALIZATION SETTINGS
# ============================================================================
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_SIZE = 8

# ============================================================================
# PREPROCESSING
# ============================================================================
# Skip processing if output file already exists
SKIP_EXISTING = True

# JPEG quality for converted images (1-100)
JPEG_QUALITY = 95
