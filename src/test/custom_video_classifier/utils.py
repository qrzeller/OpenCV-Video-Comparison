from PIL import Image
import os
import re


def remove_white_black_image(path):
    img = Image.open(path)
    if sum(img.convert("L").getextrema()) in (0, 2):
        return True
    return False


def get_filename_we_and_nf(path):
    return (os.path.splitext(os.path.basename(path))[0]).split("_")[0]


def get_filename_we_and_f(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_brand(path):
    r = re.compile("([0-9]+)([a-zA-Z]+)([0-9]+)")
    m = r.match(path)
    return m.group(2)