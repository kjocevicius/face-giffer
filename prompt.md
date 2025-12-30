# Task: Create a Python script to automate a Face Time-lapse GIF

## Project setup

- setup python tooling (`uv`) with `mise`
- setup python project with `uv`
- .gitignore `input` dir - containing the portrait photos

## Workflow

Verify each step

## Objective
I have a folder of black and white selfies (some in .heic/Apple format, some .jpg/.png) taken over several years. I need a script that:
1. Converts all HEIC files to JPEG.
2. Sorts all images chronologically (using EXIF data or filename).
3. Detects faces and aligns them so that the eyes and mouth are in the exact same coordinates in every frame.
4. Normalizes the brightness/contrast across images.
5. Generates a smooth GIF of the transformation.

## Technical Requirements
- **Libraries:** `opencv-python`, `dlib`, `numpy`, `pillow`, `pillow-heif`, `imageio`.
- **Conversion:** Use `pillow-heif` to handle Apple's HEIC files.
- **Alignment Logic:** - Use a pre-trained dlib facial landmark predictor (shape_predictor_68_face_landmarks.dat).
    - Perform an Affine Transformation to align eyes to a specific horizontal line and scale the face to a consistent size.
- **Normalization:** Apply Histogram Equalization or CLAHE to ensure the B&W tones are consistent across frames.
- **Output:** Save the aligned frames to a 'processed' folder and then compile them into a GIF (e.g., 10fps).

## Script Flow
1. **Setup:** Check for an 'input' folder and a 'output' folder.
2. **Preprocessing:** Iterate through files. If HEIC, convert to RGB JPEG. Extract "Date Taken" from EXIF to sort the list.
3. **Alignment:** For each image, find landmarks. Calculate the center of the eyes. Rotate and scale the image so the eyes are at fixed coordinates (e.g., 30% from the top, 30% and 70% from the sides).
4. **Cropping:** Crop all images to a consistent square aspect ratio (e.g., 1024x1024). ONLY IF REQUIRED - all images are portrait so not sure if needed? maybe keep portrait aspect ratio?
5. **Compilation:** Use `imageio` to create the final GIF from the aligned images.

Please provide the complete Python code and instructions on where to download the dlib .dat file.