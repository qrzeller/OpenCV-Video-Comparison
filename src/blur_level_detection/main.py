from imutils import paths
import argparse
import cv2
import os

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()


def create_blur_dir(path):
    dir = os.path.dirname(path) + '\\' + 'blur'
    if not os.path.exists(dir):
        os.makedirs(dir)


def create_new_name(path, blur_path):
    base = os.path.basename(path)
    ext = os.path.splitext(base)[1]
    file_name = os.path.splitext(base)[0]
    return blur_path + file_name + '' + ext


def check_space_in_string(input):
    if ' ' in input:
        return True
    return False


def get_all_file_dir(image_path):
    files = []
    for root, directories, filenames in os.walk(image_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    return files


def check_dir_exists(dir):
    if not os.path.isdir(dir):
        return True
    return False

def main():
    threshold = 100.0
    image_path = "C:\\Users\\Etienne\\Documents\\GitHub\\OpenCV-Video-Comparison\\src\\openvc_test\\image\\"
    blur_path = "C:\\Users\\Etienne\\Documents\\GitHub\\OpenCV-Video-Comparison\\src\\blur_level_detection\images\\blur\\"

    # Check if dir exists
    if(not check_dir_exists(image_path) | (not check_dir_exists(blur_path))):
        print('Image or blur directory not exists')
        return

    # Get all image file
    files = get_all_file_dir(image_path)

    # loop over the input images
    for imagePath in files:

        # Check wite space in path => return error
        if check_space_in_string(imagePath):
            print('White space in path !!!')
            continue

        # Load the image, convert it to grayscale, and compute the
        # focus measure of the image using the Variance of Laplacian method
        try:
            image = cv2.imread(imagePath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = variance_of_laplacian(gray)
            text = "Not Blurry"
        except:
            continue

        # If the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
        if fm < threshold:
            text = "Blurry"

        # Show image and text
        cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        print('Image path: %s, Blur level: %s' % (imagePath, str(fm)))
        # cv2.imshow("Image", image)

        # Save image
        cv2.imwrite(create_new_name(imagePath, blur_path), image)
        key = cv2.waitKey(0)


if __name__ == "__main__":
    main()