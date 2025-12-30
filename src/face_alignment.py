"""Face detection and alignment module."""

import logging
from pathlib import Path
from typing import List, Tuple, Optional

import cv2
import numpy as np
import dlib

from src.settings import (
    MODEL_PATH,
    OUTPUT_SIZE,
    EYE_Y_RATIO,
    EYE_X_RATIO_LEFT,
    EYE_X_RATIO_RIGHT,
)

logger = logging.getLogger(__name__)


class FaceAligner:
    """Detect and align faces using dlib."""
    
    def __init__(self, predictor_path: Path = MODEL_PATH):
        """Initialize detector and predictor."""
        self.predictor_path = predictor_path
        self.detector = dlib.get_frontal_face_detector()
        
        if not predictor_path.exists():
            raise FileNotFoundError(
                f"dlib model not found at {predictor_path}\n"
                "Run: uv run python -m src.download_model"
            )
        
        self.predictor = dlib.shape_predictor(str(predictor_path))
    
    def detect_face(self, image: np.ndarray) -> Optional[dlib.rectangle]:
        """Detect face in image."""
        try:
            dets = self.detector(image, 1)
            if len(dets) == 0:
                logger.warning("No face detected")
                return None
            if len(dets) > 1:
                logger.warning(f"Multiple faces detected ({len(dets)}), using largest")
                return max(dets, key=lambda d: d.width() * d.height())
            return dets[0]
        except Exception as e:
            logger.error(f"Error detecting face: {e}")
            return None
    
    def get_landmarks(self, image: np.ndarray, face: dlib.rectangle) -> Optional[np.ndarray]:
        """Get 68 facial landmarks."""
        try:
            shape = self.predictor(image, face)
            landmarks = np.array([[p.x, p.y] for p in shape.parts()])
            return landmarks
        except Exception as e:
            logger.error(f"Error getting landmarks: {e}")
            return None
    
    def align_face(
        self,
        image: np.ndarray,
        landmarks: np.ndarray,
        output_size: Tuple[int, int] = OUTPUT_SIZE,
        eye_y_ratio: float = EYE_Y_RATIO,
        eye_x_ratio_left: float = EYE_X_RATIO_LEFT,
        eye_x_ratio_right: float = EYE_X_RATIO_RIGHT
    ) -> Optional[np.ndarray]:
        """
        Align face using affine transformation.
        """
        try:
            # Get current eye positions
            left_eye = landmarks[36:42].mean(axis=0)
            right_eye = landmarks[42:48].mean(axis=0)
            
            # Target eye positions
            target_left_x = output_size[0] * eye_x_ratio_left
            target_right_x = output_size[0] * eye_x_ratio_right
            target_y = output_size[1] * eye_y_ratio
            
            # Calculate rotation angle
            dy = right_eye[1] - left_eye[1]
            dx = right_eye[0] - left_eye[0]
            angle = np.arctan2(dy, dx) * 180 / np.pi
            
            # Calculate scale
            current_eye_dist = np.sqrt(dx**2 + dy**2)
            target_eye_dist = target_right_x - target_left_x
            scale = target_eye_dist / current_eye_dist
            
            # Get rotation matrix
            center = left_eye + (right_eye - left_eye) / 2
            rot_mat = cv2.getRotationMatrix2D(tuple(center), angle, scale)
            
            # Adjust translation
            rot_mat[0, 2] += target_left_x - left_eye[0]
            rot_mat[1, 2] += target_y - left_eye[1]
            
            # Apply affine transformation
            aligned = cv2.warpAffine(image, rot_mat, output_size, borderMode=cv2.BORDER_CONSTANT)
            
            return aligned
        except Exception as e:
            logger.error(f"Error aligning face: {e}")
            return None
    
    def process_image(
        self,
        image_path: Path,
        output_size: Tuple[int, int] = OUTPUT_SIZE
    ) -> Optional[np.ndarray]:
        """Load, detect, and align face in image."""
        try:
            image = cv2.imread(str(image_path))
            if image is None:
                logger.error(f"Could not load image: {image_path}")
                return None
            
            # Convert to grayscale for detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect face
            face = self.detect_face(gray)
            if face is None:
                logger.warning(f"No face detected in {image_path.name}")
                return None
            
            # Get landmarks
            landmarks = self.get_landmarks(gray, face)
            if landmarks is None:
                logger.warning(f"Could not get landmarks for {image_path.name}")
                return None
            
            # Align face
            aligned = self.align_face(image, landmarks, output_size)
            if aligned is None:
                logger.warning(f"Could not align face in {image_path.name}")
                return None
            
            logger.info(f"Successfully aligned {image_path.name}")
            return aligned
        except Exception as e:
            logger.error(f"Error processing {image_path}: {e}")
            return None


def align_all_faces(
    image_paths: List[Path],
    model_path: Path = MODEL_PATH,
    output_size: Tuple[int, int] = OUTPUT_SIZE
) -> List[np.ndarray]:
    """Align all faces in a list of images."""
    logger.info("Starting face alignment...")
    
    aligner = FaceAligner(model_path)
    aligned_images = []
    
    for i, image_path in enumerate(image_paths, 1):
        logger.info(f"Processing {i}/{len(image_paths)}: {image_path.name}")
        aligned = aligner.process_image(image_path, output_size)
        if aligned is not None:
            aligned_images.append(aligned)
    
    logger.info(f"Successfully aligned {len(aligned_images)}/{len(image_paths)} images")
    return aligned_images
