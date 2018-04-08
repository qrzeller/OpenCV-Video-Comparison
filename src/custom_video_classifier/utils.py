from PIL import Image


def remove_white_black_image(path):
    img = Image.open(path)
    if sum(img.convert("L").getextrema()) in (0, 2):
        return True
    return False