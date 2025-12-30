"""Face Giffer - Time-lapse GIF from portrait selfies."""

from src.settings import *
from src.preprocessing import preprocess_images
from src.face_alignment import align_all_faces, FaceAligner
from src.normalization import normalize_brightness, create_gif, save_processed_frames
