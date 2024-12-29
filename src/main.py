import os
import tifffile
import cv2
import logging
from lib.circle_detector import get_vertex
from concurrent.futures import ThreadPoolExecutor


def get_files_recursive(directory):
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def tiff_to_array(file_path):
    return cv2.imread(file_path)


def get_image_patches(image_array, patch_size, step_size):
    """
    Extract patches of a specific size from a single image.

    Args:
        image_array (np.ndarray): Input image as a NumPy array.
        patch_size (tuple): Size of each patch (height, width).
        step_size (tuple): Step size (vertical_step, horizontal_step).

    Returns:
        list: A list of image patches as NumPy arrays.
    """
    rectangles = get_vertex(
        image_array, buffer=0
    )  # Get the rectangles that contain circles
    patches = []
    patch_height, patch_width = patch_size
    step_y, step_x = step_size

    image_height, image_width = image_array.shape[:2]

    for y in range(0, image_height - patch_height + 1, step_y):
        for x in range(0, image_width - patch_width + 1, step_x):
            patch = image_array[y : y + patch_height, x : x + patch_width]

            # Check if any rectangle overlaps with the current patch
            for rect in rectangles:
                rect_x, rect_y, rect_w, rect_h = (
                    rect  # Unpack rectangle (x, y, width, height)
                )

                # Check if the circle's rectangle is within the patch's range
                if (
                    rect_x + rect_w
                    > x  # Right edge of the rect is right of the patch left
                    and rect_x
                    < x
                    + patch_width  # Left edge of the rect is left of the patch right
                    and rect_y + rect_h
                    > y  # Bottom edge of the rect is below the patch top
                    and rect_y
                    < y + patch_height  # Top edge of the rect is above the patch bottom
                ):
                    patches.append(patch)

                    # Debug: Log patch dimensions and type
                    logging.info(
                        f"Processing patch at ({y}, {x}), shape: {patch.shape}, dtype: {patch.dtype}"
                    )
                    break  # No need to check other rectangles once we found one inside the patch

    logging.info(f"Total patches containing circles: {len(patches)}")
    return patches


def save_patches(patches, save_dir, image_index):
    """
    Save the extracted patches to the specified directory as TIFF files.

    Args:
        patches (list): List of image patches as NumPy arrays.
        save_dir (str): Directory to save the patches.
        image_index (int): Index of the image being processed.
    """
    image_dir = os.path.join(save_dir, f"image_{image_index + 1}")
    os.makedirs(image_dir, exist_ok=True)

    for i, patch in enumerate(patches):
        patch_filename = os.path.join(image_dir, f"patch_{i + 1}.tiff")
        tifffile.imwrite(patch_filename, patch)
        print(f"Saved patch: {patch_filename}")


def process_image(file_path, patch_size, step_size, output_dir, image_index):
    image = tiff_to_array(file_path)
    print(f"Processing image: {file_path}, shape: {image.shape}")
    patches = get_image_patches(image, patch_size, step_size)
    save_patches(patches, output_dir, image_index)


def main():
    INPUT_PATH = r"data/"
    PATCH_X, PATCH_Y = 512, 512
    STEP_SIZE_X, STEP_SIZE_Y = 32, 32
    OUTPUT_DIR = r"subpatches/"
    NUM_THREADS = 8

    all_files = get_files_recursive(INPUT_PATH)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for idx, file_path in enumerate(all_files):
            futures.append(
                executor.submit(
                    process_image,
                    file_path,
                    (PATCH_X, PATCH_Y),
                    (STEP_SIZE_X, STEP_SIZE_Y),
                    OUTPUT_DIR,
                    idx,
                )
            )

        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
