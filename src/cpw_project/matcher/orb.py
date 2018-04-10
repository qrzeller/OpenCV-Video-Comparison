import cv2
import utils
from datetime import datetime


# TODO must return dico_match and the scene_files cleaned up
def orb_matcher(scenes_path, dico_match, result_json_file):

    # Get all image file recursive
    scenes_files = utils.get_files_rec(scenes_path)

    progress = 0
    maximum = len(scenes_files)

    for base_file in scenes_files:
        progress = progress + 1
        for compare_file in scenes_files:

            # Check if base file is not compare with itself
            if utils.get_video_name(base_file) != utils.get_video_name(compare_file):
                match = detect_match(base_file, compare_file)
                if len(match) > 0:
                    dico_match.setdefault(utils.get_video_name(base_file), []).append(compare_file + ";orb")
        print("[%s] Current process: %s/%s" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), str(progress), str(maximum)))
        utils.save_json_match(dico_match, result_json_file)
    return dico_match


def orb_matcher_old(base_file, compare_file):

    # Load image and ensure grayscale(0)
    base = cv2.imread(base_file, 0)
    compare = cv2.imread(compare_file, 0)

    # Create ORB detector with 1000 keypoints with a scaling pyramid factor of 1.2
    orb = cv2.ORB_create()

    # Detect keypoints for each image
    (kp1, des1) = orb.detectAndCompute(base, None)
    (kp2, des2) = orb.detectAndCompute(compare, None)

    # Create matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # if des(1|2) == None => error
    #if (des1 is not None) and (des2 is not None):

    # Perform matching
    matches = bf.match(des1, des2)

    # Sort the matches based on distance. Least distance is better
    dist = [m.distance for m in matches]
    thres_dist = (sum(dist) / len(dist)) * 0.5
    matches = [m for m in matches if m.distance < thres_dist]
    return matches


def detect_match(base_file, compare_file):

    # Load image and ensure grayscale(0)
    base = cv2.imread(base_file, 0)
    compare = cv2.imread(compare_file, 0)

    # Create ORB detector with 1000 keypoints with a scaling pyramid factor of 1.2
    orb = cv2.ORB_create()

    # Detect keypoints for each image
    (kp1, des1) = orb.detectAndCompute(base, None)
    (kp2, des2) = orb.detectAndCompute(compare, None)

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
