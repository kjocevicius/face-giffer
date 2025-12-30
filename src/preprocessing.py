"""Preprocessing module for image conversion and sorting."""

import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
import pillow_heif

from src.settings import SKIP_EXISTING, JPEG_QUALITY

logger = logging.getLogger(__name__)


def get_exif_datetime(image_path: Path) -> Optional[datetime]:
    """Extract datetime from image EXIF data."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        if exif_data is None:
            return None
        
        # Tag 306 is DateTime, 36867 is DateTimeOriginal
        for tag_id, value in exif_data.items():
            if tag_id in (306, 36867):
                try:
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                except (ValueError, TypeError):
                    return None
    except Exception as e:
        logger.debug(f"Could not extract EXIF from {image_path}: {e}")
        return None


def get_heic_exif_datetime(heic_path: Path) -> Optional[datetime]:
    """Extract datetime from HEIC EXIF data."""
    try:
        pillow_heif.register_heif_opener()
        image = Image.open(heic_path)
        exif_data = image.getexif()
        
        if exif_data is None:
            return None
        
        # Tag 306 is DateTime, 36867 is DateTimeOriginal
        for tag_id in (36867, 306):
            if tag_id in exif_data:
                try:
                    return datetime.strptime(exif_data[tag_id], "%Y:%m:%d %H:%M:%S")
                except (ValueError, TypeError):
                    pass
        return None
    except Exception as e:
        logger.debug(f"Could not extract EXIF from HEIC {heic_path}: {e}")
        return None


def get_file_datetime(image_path: Path) -> datetime:
    """Fallback: get datetime from file modification time."""
    stat = image_path.stat()
    return datetime.fromtimestamp(stat.st_mtime)


def heic_to_jpeg(heic_path: Path, output_path: Path) -> bool:
    """Convert HEIC image to JPEG."""
    try:
        pillow_heif.register_heif_opener()
        image = Image.open(heic_path)
        
        # Preserve EXIF data
        exif = image.info.get('exif', None)
        
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        if exif:
            image.save(output_path, "JPEG", quality=JPEG_QUALITY, exif=exif)
        else:
            image.save(output_path, "JPEG", quality=JPEG_QUALITY)
        
        logger.info(f"Converted {heic_path.name} to {output_path.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to convert {heic_path}: {e}")
        return False


def preprocess_images(input_dir: Path, processed_dir: Path) -> List[Path]:
    """
    Preprocess all images: convert HEIC to JPEG and sort chronologically.
    
    Returns:
        List of processed image paths, sorted by capture date
    """
    logger.info("Starting image preprocessing...")
    processed_dir.mkdir(exist_ok=True)
    
    # Collect all images with their dates
    image_dates: List[tuple[Path, datetime]] = []
    
    # Step 1: Process HEIC files
    heic_files = list(input_dir.glob("*.[Hh][Ee][Ii][Cc]"))
    logger.info(f"Found {len(heic_files)} HEIC files")
    
    skipped = 0
    converted = 0
    
    for heic_file in heic_files:
        output_path = processed_dir / heic_file.with_suffix(".jpg").name
        
        # Get date from original HEIC before conversion
        date = get_heic_exif_datetime(heic_file) or get_file_datetime(heic_file)
        
        # Skip if already exists
        if SKIP_EXISTING and output_path.exists():
            logger.debug(f"Skipping {heic_file.name} - already converted")
            skipped += 1
            image_dates.append((output_path, date))
            continue
        
        if heic_to_jpeg(heic_file, output_path):
            converted += 1
            image_dates.append((output_path, date))
    
    if skipped > 0:
        logger.info(f"Skipped {skipped} already converted HEIC files")
    if converted > 0:
        logger.info(f"Converted {converted} HEIC files")
    
    # Step 2: Copy existing JPEG/PNG files
    copied = 0
    for pattern in ["*.[Jj][Pp][Gg]", "*.[Jj][Pp][Ee][Gg]", "*.[Pp][Nn][Gg]"]:
        for image_file in input_dir.glob(pattern):
            output_path = processed_dir / image_file.name
            
            # Get date from original
            date = get_exif_datetime(image_file) or get_file_datetime(image_file)
            
            # Skip if already exists
            if SKIP_EXISTING and output_path.exists():
                logger.debug(f"Skipping {image_file.name} - already exists")
                image_dates.append((output_path, date))
                continue
            
            try:
                img = Image.open(image_file)
                exif = img.info.get('exif', None)
                
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                if exif:
                    img.save(output_path, quality=JPEG_QUALITY, exif=exif)
                else:
                    img.save(output_path, quality=JPEG_QUALITY)
                
                copied += 1
                image_dates.append((output_path, date))
                logger.info(f"Copied {image_file.name}")
            except Exception as e:
                logger.error(f"Failed to process {image_file}: {e}")
    
    if copied > 0:
        logger.info(f"Copied {copied} JPG/PNG files")
    
    # Step 3: Sort by capture date
    image_dates.sort(key=lambda x: x[1])
    processed_images = [path for path, _ in image_dates]
    
    logger.info(f"Processed {len(processed_images)} images total")
    
    # Log first and last few for verification
    if len(processed_images) >= 2:
        first_date = image_dates[0][1].strftime('%Y-%m-%d')
        last_date = image_dates[-1][1].strftime('%Y-%m-%d')
        logger.info(f"Date range: {first_date} to {last_date}")
    
    return processed_images
