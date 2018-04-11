from matcher.ihcolorutils.rgbhistogram import RGBHistogram
from matcher.ihcolorutils.searcher import Searcher
from datetime import datetime
import pickle
import cv2
import utils
import json
import networkx as nx
from networkx import readwrite


def histo_matcher(scenes_path, indexer_path, result_match_path, threshold=0.19):
    index_images(scenes_path, indexer_path)
    search_match(indexer_path, result_match_path, threshold)


def index_images(scenes_path, index_path):
    # initialize the index dictionary to store our our quantifed
    # images, with the 'key' of the dictionary being the image
    # filename and the 'value' our computed features
    index = {}

    # initialize our image descriptor -- a 3D RGB histogram with
    # 8 bins per channel
    desc = RGBHistogram([8, 8, 8])

    # use glob to grab the image paths and loop over them
    # for imagePath in glob.glob(scenes_path + "/*.png"):
    for file in utils.get_files_rec(scenes_path):

        # Check if not black nor white image
        if not utils.remove_white_black_image(file):
            # extract our unique image ID (i.e. the filename)
            k = file[file.rfind("/") + 1:]

            # load the image, describe it using our RGB histogram
            # descriptor, and update the index
            image = cv2.imread(file)
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


def search_match(indexer_path, result_match_path, threshold=0.15):

    # Graf to process match
    G = nx.MultiGraph()

    # load the index and initialize our searcher
    with open(indexer_path, 'rb') as handle:
        index = pickle.load(handle)
    searcher = Searcher(index)

    # loop over images in the index -- we will use each one as
    # a query image
    max = len(index)
    count = 0
    for (query, queryFeatures) in index.items():

        # Show progress
        count = count + 1
        print("[%s] progress image %s/%s" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), count, max))

        # perform the search using the current query
        results = searcher.search(queryFeatures)

        # load the query image and display it
        print("[%s] query: %s" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), query))

        # loop over the top ten results
        for j in range(0, 10):

            # grab the result (we are using row-major order) and
            # load the result image
            (score, image_name) = results[j]
            path = "%s" % (image_name)

            # Check if don't compare same video image
            base_brand = utils.get_brand(utils.get_filename_we(query))
            compare_brand = utils.get_brand(utils.get_filename_we(image_name))
            if base_brand != compare_brand:

                # Check if we don't compare with the same video
                # Add threshold to avoid wrong match
                if score <= threshold:
                    G.add_edge(base_brand, compare_brand, weight=score)
                    print("match")

    # Save graph relation
    with open(result_match_path, 'w') as f:
        f.write(json.dumps(readwrite.json_graph.node_link_data(G)))