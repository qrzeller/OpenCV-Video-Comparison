import cv2

def detect_match(base_image, compare_image):

    # Create ORB detector with 1000 keypoints with a scaling pyramid factor of 1.2
    orb = cv2.ORB_create()

    # Detect keypoints for each image
    (kp1, des1) = orb.detectAndCompute(base_image, None)
    (kp2, des2) = orb.detectAndCompute(compare_image, None)

    # Create matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # if des(1|2) == None => error
    good = []
    if (des1 is not None) and (des2 is not None):

        # Perform matching
        matches = bf.match(des1, des2)

        # Sort the matches based on distance. Least distance is better
        for m in matches:
            if m.distance < 0.65:
                good.append(m)
    return good
