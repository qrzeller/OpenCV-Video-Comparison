from skimage.measure import compare_ssim


def detect_match(base_image, compare_image):

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(base_image, compare_image, full=True)
    if score > 0.8:
        return True, score
    return False, score
