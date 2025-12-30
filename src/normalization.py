"""Image normalization and GIF compilation."""

import logging
from pathlib import Path
from typing import List

import cv2
import numpy as np
import imageio

from src.settings import CLAHE_CLIP_LIMIT, CLAHE_TILE_SIZE, GIF_FPS, GIF_LOOP

logger = logging.getLogger(__name__)


def clahe_normalize(
    image: np.ndarray,
    clip_limit: float = CLAHE_CLIP_LIMIT,
    tile_size: int = CLAHE_TILE_SIZE
) -> np.ndarray:
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)."""
    try:
        if len(image.shape) == 3 and image.shape[2] == 3:
            # BGR to LAB
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
            l_clahe = clahe.apply(l)
            
            # Merge back
            lab_clahe = cv2.merge([l_clahe, a, b])
            result = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
            return result
        else:
            # Grayscale image
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
            return clahe.apply(image)
    except Exception as e:
        logger.error(f"Error applying CLAHE: {e}")
        return image


def normalize_brightness(images: List[np.ndarray], clip_limit: float = CLAHE_CLIP_LIMIT) -> List[np.ndarray]:
    """Apply brightness normalization to all images."""
    logger.info("Normalizing brightness across images...")
    normalized = []
    
    for i, image in enumerate(images, 1):
        if i % 20 == 0 or i == len(images):
            logger.info(f"Normalizing {i}/{len(images)}")
        normalized_img = clahe_normalize(image, clip_limit=clip_limit)
        normalized.append(normalized_img)
    
    logger.info("Brightness normalization complete")
    return normalized


def create_gif(
    images: List[np.ndarray],
    output_path: str,
    fps: int = GIF_FPS,
    loop: int = GIF_LOOP
) -> bool:
    """
    Create animated GIF from images.
    """
    logger.info(f"Creating GIF with {len(images)} frames at {fps} fps...")
    
    try:
        if not images:
            logger.error("No images to create GIF")
            return False
        
        # Convert BGR to RGB for imageio
        rgb_images = []
        for img in images:
            if len(img.shape) == 3 and img.shape[2] == 3:
                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            rgb_images.append(rgb)
        
        # Create GIF
        duration = 1000 / fps  # Duration per frame in milliseconds
        imageio.mimsave(
            output_path,
            rgb_images,
            format='GIF',
            duration=duration,
            loop=loop
        )
        
        file_size = Path(output_path).stat().st_size / (1024 * 1024)
        logger.info(f"GIF created successfully: {output_path} ({file_size:.2f} MB)")
        return True
    except Exception as e:
        logger.error(f"Error creating GIF: {e}")
        return False


def save_processed_frames(
    images: List[np.ndarray],
    output_dir: Path,
    prefix: str = "frame"
) -> List[Path]:
    """Save individual processed frames for inspection."""
    logger.info(f"Saving {len(images)} frames to {output_dir}...")
    saved_paths = []
    
    try:
        output_dir.mkdir(exist_ok=True)
        for i, image in enumerate(images, 1):
            frame_num = str(i).zfill(4)
            output_path = output_dir / f"{prefix}_{frame_num}.jpg"
            
            success = cv2.imwrite(str(output_path), image)
            if success:
                saved_paths.append(output_path)
                logger.debug(f"Saved {output_path.name}")
            else:
                logger.error(f"Failed to save {output_path}")
        
        logger.info(f"Saved {len(saved_paths)}/{len(images)} frames")
        return saved_paths
    except Exception as e:
        logger.error(f"Error saving frames: {e}")
        return saved_paths
