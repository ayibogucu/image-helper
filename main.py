import cv2
import os


def plot_batch(array_batch, window_name: str):
    for array in array_batch:
        array_normalized = cv2.normalize(
            src=array,
            dst=None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX,
            dtype=cv2.CV_8U,
        )

        array_normalized = array_normalized.astype("uint8")

        cv2.imshow(window_name, array_normalized)
        while True:
            key = cv2.waitKey(100)  # Check every 100 ms
            if key != -1:  # If a key is pressed
                break
            # Check if the window was closed
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break


def get_files_recursive(directory):
    all_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))

    return all_files


def get_image_patches(image_path, patch_size, step_size):
    """
    Extract patches of a specific size from an image with a given step size.

    Args:
        image_path (str): Path to the input image.
        patch_size (tuple): Size of each patch (height, width).
        step_size (tuple): Step size (vertical_step, horizontal_step).

    Returns:
        list: A list of image patches as NumPy arrays.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or path is incorrect.")

    patches = []
    patch_height, patch_width = patch_size
    step_y, step_x = step_size

    # Get the dimensions of the image
    image_height, image_width, _ = image.shape

    # Iterate over the image to extract patches
    for y in range(0, image_height - patch_height + 1, step_y):
        for x in range(0, image_width - patch_width + 1, step_x):
            patch = image[y : y + patch_height, x : x + patch_width]
            patches.append(patch)

    return patches


def save_patches(patches, save_dir):
    """
    Save the extracted patches to the specified directory.

    Args:
        patches (list): List of image patches as NumPy arrays.
        save_dir (str): Directory to save the patches.
    """
    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    for i, patch in enumerate(patches):
        patch_filename = os.path.join(save_dir, f"patch_{i + 1}.jpg")
        cv2.imwrite(patch_filename, patch)


def main():
    INPUT_PATH = r"data/"
    PATCH_X, PATCH_Y = 256, 256
    STEP_SIZE_X, STEP_SIZE_Y = 128, 128
    OUTPUT_DIR = r"subpatches/"

    all_files = get_files_recursive(INPUT_PATH)
    for i in range(len(all_files)):
        patches = get_image_patches(
            all_files[i], (PATCH_X, PATCH_Y), (STEP_SIZE_X, STEP_SIZE_Y)
        )

        # plot_batch(patches, "wazzaaaaap")

        output_dir = f"{OUTPUT_DIR}/{i+1}"

        save_patches(patches, output_dir)

    cv2.destroyAllWindows()


main()
