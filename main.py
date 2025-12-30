#!/usr/bin/env python3
"""
Face Time-lapse GIF Generator
Converts a folder of selfies into an animated GIF with aligned faces.
"""

import sys
import logging
from pathlib import Path
from typing import List

import numpy as np

from src.settings import (
    INPUT_DIR,
    OUTPUT_DIR,
    PROCESSED_DIR,
    MODEL_PATH,
    OUTPUT_SIZE,
    GIF_FPS,
)
from src.preprocessing import preprocess_images
from src.face_alignment import align_all_faces
from src.normalization import normalize_brightness, create_gif

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FaceGiffer:
    """Main class for face alignment and GIF generation."""

    def __init__(
        self,
        input_dir: Path = INPUT_DIR,
        output_dir: Path = OUTPUT_DIR,
        processed_dir: Path = PROCESSED_DIR
    ):
        """Initialize FaceGiffer with directories."""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.processed_dir = Path(processed_dir)
        self.model_path = MODEL_PATH
        
        # Create directories if they don't exist
        self.output_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
        
    def setup(self) -> bool:
        """Setup and verify all requirements."""
        logger.info("Checking setup...")
        
        if not self.input_dir.exists():
            logger.error(f"Input directory '{self.input_dir}' not found")
            return False
        
        if not self.model_path.exists():
            logger.error(f"dlib model not found at {self.model_path}")
            logger.info("Run: uv run python -m src.download_model")
            return False
        
        image_count = sum(
            len(list(self.input_dir.glob(pattern)))
            for pattern in ["*.[Hh][Ee][Ii][Cc]", "*.[Jj][Pp][Gg]", "*.[Pp][Nn][Gg]"]
        )
        
        if image_count == 0:
            logger.error(f"No images found in '{self.input_dir}'")
            return False
        
        logger.info(f"Found {image_count} images in '{self.input_dir}'")
        return True

    def preprocess(self) -> List[Path]:
        """Convert HEIC to JPEG and sort chronologically."""
        return preprocess_images(self.input_dir, self.processed_dir)

    def align_faces(self, images: List[Path]) -> List[np.ndarray]:
        """Detect and align faces."""
        return align_all_faces(images, self.model_path, OUTPUT_SIZE)

    def normalize(self, images: List[np.ndarray]) -> List[np.ndarray]:
        """Apply CLAHE normalization."""
        return normalize_brightness(images)

    def create_output(
        self,
        images: List[np.ndarray],
        output_name: str = "timelapse.gif",
        fps: int = GIF_FPS
    ) -> bool:
        """Create animated GIF from images."""
        if not images:
            logger.error("No images to create GIF")
            return False
        
        output_path = str(self.output_dir / output_name)
        return create_gif(images, output_path, fps=fps)

    def run(self):
        """Main workflow."""
        logger.info("Starting Face Giffer workflow...")
        logger.info(f"Output size: {OUTPUT_SIZE[0]}x{OUTPUT_SIZE[1]}")
        
        if not self.setup():
            sys.exit(1)
        
        # Step 1: Preprocess
        logger.info("Step 1/4: Preprocessing images...")
        images = self.preprocess()
        if not images:
            logger.error("No images after preprocessing")
            sys.exit(1)
        
        # Step 2: Align faces
        logger.info("Step 2/4: Aligning faces...")
        aligned_images = self.align_faces(images)
        if not aligned_images:
            logger.error("Failed to align any faces")
            sys.exit(1)
        
        # Step 3: Normalize brightness
        logger.info("Step 3/4: Normalizing brightness...")
        normalized_images = self.normalize(aligned_images)
        
        # Step 4: Create GIF
        logger.info("Step 4/4: Creating GIF...")
        if self.create_output(normalized_images):
            logger.info(f"✓ Successfully created GIF: {self.output_dir}/timelapse.gif")
        else:
            logger.error("Failed to create GIF")
            sys.exit(1)


if __name__ == "__main__":
    giffer = FaceGiffer()
    giffer.run()
