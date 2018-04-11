import cv2
import utils


# Load the image, convert it to grayscale, and compute the
# focus measure of the image using the Variance of Laplacian method
def blur_detection(scenes_path, blur_threshold=100.0):

    # Get all image file recursive
    scenes_files = utils.get_files_rec(scenes_path)

    blur_files = []
    for file in scenes_files:
        image = cv2.imread(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)

        # If the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
        if fm < blur_threshold:
            blur_files.append(file)
    return blur_files


# compute the Laplacian of the image and then return the focus
# measure, which is simply the variance of the Laplacian
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()
