#!/usr/bin/env python3
"""Utility to download dlib face landmark predictor model."""

import logging
import sys
from pathlib import Path
import urllib.request
import bz2
import shutil

from src.settings import MODEL_PATH, MODEL_URL

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

MODEL_BZ2 = f"{MODEL_PATH}.bz2"


def download_model():
    """Download and extract dlib face landmark predictor."""
    # Check if already exists
    if MODEL_PATH.exists():
        logger.info(f"✓ Model already exists at {MODEL_PATH}")
        return True
    
    logger.info("Downloading dlib face landmark predictor...")
    logger.info(f"URL: {MODEL_URL}")
    logger.info(f"Filename: {MODEL_PATH} (~100 MB)")
    
    try:
        logger.info("Downloading...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_BZ2)
        
        logger.info("Extracting BZ2 archive...")
        with bz2.open(MODEL_BZ2, 'rb') as f_in:
            with open(MODEL_PATH, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Clean up BZ2 file
        Path(MODEL_BZ2).unlink()
        
        logger.info(f"✓ Successfully downloaded and extracted: {MODEL_PATH}")
        return True
    
    except Exception as e:
        logger.error(f"✗ Failed to download: {e}")
        logger.info("\nManual download instructions:")
        logger.info(f"1. Download from: {MODEL_URL}")
        logger.info(f"2. Extract {MODEL_PATH}.bz2")
        logger.info("3. Place the .dat file in the project root")
        return False


if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
