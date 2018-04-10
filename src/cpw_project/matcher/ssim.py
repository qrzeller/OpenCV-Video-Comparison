import utils
from datetime import datetime
from skimage.measure import compare_ssim
import cv2


# TODO must return dico_match and the scene_files cleaned up
def ssim_matcher(scenes_path, dico_match, result_json_file):

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
                if match:
                    dico_match.setdefault(utils.get_video_name(base_file), []).append(compare_file + ";ssim")
        print("[%s] Current process: %s/%s" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), str(progress), str(maximum)))
        utils.save_json_match(dico_match, result_json_file)
    return dico_match


def detect_match(base_file, compare_file):

    # Load image and ensure grayscale(0)
    base = cv2.imread(base_file, 0)
    compare = cv2.imread(compare_file, 0)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(base, compare, full=True)
    if score > 0.8:
        return True
    return False
