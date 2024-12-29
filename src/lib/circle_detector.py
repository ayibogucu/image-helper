import numpy as np
import cv2


def _preproccess(
    image: np.ndarray,
    blur_kernel: tuple = (51, 51),
    threshold_blocksize: int = 11,
    morphology_kernel: tuple = (5, 5),
):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    blur = cv2.GaussianBlur(gray, blur_kernel, cv2.BORDER_DEFAULT)

    # Adaptive thresholding
    binary = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        threshold_blocksize,
        2,
    )

    # Morphological closing to enhance circle shapes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morphology_kernel)
    morphed = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return morphed


def _get_circle(
    image: np.ndarray,
    dp=1,
    minDist=200,
    param1=50,
    param2=25,
    minRadius=50,
    maxRadius=200,
):
    preprocessed_image = _preproccess(image)

    circles = cv2.HoughCircles(
        preprocessed_image,
        cv2.HOUGH_GRADIENT,
        dp,
        minDist=minDist,
        param1=param1,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius,
    )

    return circles


def get_vertex(
    image: np.ndarray,
    dp=1,
    minDist=200,
    param1=50,
    param2=25,
    minRadius=50,
    maxRadius=200,
    buffer=30,
):
    preprocessed_image = _preproccess(image)

    circles = cv2.HoughCircles(
        preprocessed_image,
        cv2.HOUGH_GRADIENT,
        dp,
        minDist=minDist,
        param1=param1,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius,
    )

    list = []
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for x, y, r in circles:
            list.append(
                (x - r - buffer, y - r - buffer, 2 * r + 2 * buffer, 2 * r + 2 * buffer)
            )
    return list
