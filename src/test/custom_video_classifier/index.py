# python index.py --dataset images --index index.cpickle
from pyimagesearch.rgbhistogram import RGBHistogram
from datetime import datetime
import pickle
import glob
import cv2
import utils


def index_images(image_path, index_path):

    # initialize the index dictionary to store our our quantifed
    # images, with the 'key' of the dictionary being the image
    # filename and the 'value' our computed features
    index = {}

    # initialize our image descriptor -- a 3D RGB histogram with
    # 8 bins per channel
    desc = RGBHistogram([8, 8, 8])

    # use glob to grab the image paths and loop over them
    for imagePath in glob.glob(image_path + "/*.png"):

        # Check if not black nor white image
        if not utils.remove_white_black_image(imagePath):

            # extract our unique image ID (i.e. the filename)
            k = imagePath[imagePath.rfind("/") + 1:]

            # load the image, describe it using our RGB histogram
            # descriptor, and update the index
            image = cv2.imread(imagePath)
            features = desc.describe(image)
            index[k] = features

    # we are now done indexing our image -- now we can write our
    # index to disk
    f = open(index_path, "wb")
    f.write(pickle.dumps(index))
    f.close()

    # show how many images we indexed
    # print("done...indexed %d images" % (len(index)))
    print("[%s] done...indexed %d images" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), len(index)))
