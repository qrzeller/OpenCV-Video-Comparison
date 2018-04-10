import cv2


# Load the image, convert it to grayscale, and compute the
# focus measure of the image using the Variance of Laplacian method
def blur_detection(files):
    threshold = 100.0
    blur_files = []
    for file in files:
        image = cv2.imread(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        text = "Not Blurry"

        # If the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
        if fm < threshold:
            text = "Blurry"
            blur_files.append(file)
    return clean_up_list(files, blur_files)


# compute the Laplacian of the image and then return the focus
# measure, which is simply the variance of the Laplacian
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def clean_up_list(files, blur_files):
    for blur_file in blur_files:
        try:
            files.remove(blur_file)
        except ValueError:
            continue
    return files
