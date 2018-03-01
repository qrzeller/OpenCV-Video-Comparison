import cv2


def put_text_on_image(opencv_img, text):
    """ Write text with correct size and thickness on given image """
    def __get_origin():
        origin = tuple(int(i / 10) for i in opencv_img.shape[:2])
        return origin

    font_size = max(opencv_img.shape[0]/1000, 0.8)
    cv2.putText(
        opencv_img,
        text,
        org=__get_origin(),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=font_size,
        color=(0, 255, 0),
        thickness=max(int(opencv_img.shape[0]/500), 2),
        lineType=cv2.LINE_AA,
        bottomLeftOrigin=False
    )


def put_text_on_image_file(filepath, text, overwrite=False):
    """ Write text with correct size and thickness on image at given path """
    img = cv2.imread(filepath)
    put_text_on_image(img, text)
    if overwrite:
        cv2.imwrite(filepath, img)
    return img

