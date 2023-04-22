import cv2
import easyocr
import logging

logger = logging.getLogger(__name__)


def extract_text_from_mp4(mp4_path, frame_capture_frequency=40):
    reader = easyocr.Reader(["fr"], model_storage_directory="./.easyOCR/")
    logger.info("Initialized easyocr reader")
    video = cv2.VideoCapture(mp4_path)
    logger.info(f"loaded mp4 video from {mp4_path}")
    frames_text = []
    num_frame = 0
    img_scaling_factor = 0.4  # Lower processing time and equal performance

    while video.isOpened():
        num_frame += 1
        is_frame, frame = video.read()
        if is_frame and (num_frame % frame_capture_frequency == 0):
            resized_frame = resize_cv2image(frame, img_scaling_factor)
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            _, binary_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)

            text = " ".join(reader.readtext(binary_frame, detail=0))
            frames_text.append(text)
            logger.info(f"Extracted text for frame {len(frames_text)}")
        elif not is_frame:
            break
    video.release()
    all_text = " ".join(frames_text)
    text = remove_duplicate_words(all_text)
    logger.info("Merged text from frames")
    logger.debug(f"text={text}")
    return text


def resize_cv2image(cv2_image, scaling_factor):
    image_shape = cv2_image.shape
    new_shape = (
        int(image_shape[1] * scaling_factor),
        int(image_shape[0] * scaling_factor),
    )
    image_resized = cv2.resize(cv2_image, new_shape)
    logger.info(f"resized image from {image_shape} to {new_shape}")
    return image_resized


def remove_duplicate_words(text):
    # Keep same order
    return " ".join(dict.fromkeys(text.split(" ")))
