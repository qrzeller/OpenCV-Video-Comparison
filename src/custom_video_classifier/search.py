# python search.py --dataset images --index index.cpickle
from pyimagesearch.searcher import Searcher
from datetime import datetime
import pickle
import utils


def search_match(index_path, threshold=0.2):

    # load the index and initialize our searcher
    with open(index_path, 'rb') as handle:
        index = pickle.load(handle)
    searcher = Searcher(index)

    # loop over images in the index -- we will use each one as
    # a query image
    max = len(index)
    count  = 0
    for (query, queryFeatures) in index.items():

        # Show progress
        count = count + 1
        print("[%s] progress image %s/%s" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), count, max))


        # Check if not black nor white image
        if not utils.remove_white_black_image(query):

            # perform the search using the current query
            results = searcher.search(queryFeatures)

            # load the query image and display it
            print("[%s] query: %s" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), query))

            # Get filename we (base file) and brand name
            brand_base = utils.get_filename_we_and_nf(query)
            b1 = utils.get_brand(brand_base)

            # loop over the top ten results
            error = False
            match = 0
            for j in range(0, 10):

                # grab the result (we are using row-major order) and
                # load the result image
                (score, image_name) = results[j]
                path = "%s" % (image_name)

                # Get filename we (file which match with base file) and brand name
                brand_compare = utils.get_filename_we_and_nf(path)
                b2 = utils.get_brand(brand_compare)

                # Check if the first match found always match, even if the threshold (score) is
                # higher than the base threshold.
                # If we pass by this if => we cannot trust that the first match always match
                if (j == 0) and (b1 != b2):
                    print("[%s] First match not always match !!!" % (str(datetime.now().strftime("%d-%m-%Y %H:%M"))))
                    error = True

                # Check if we don't compare with the same video
                # Add threshold to avoid wrong match
                if (brand_base != brand_compare) and score <= threshold:
                    match = match + 1

                    # Check threshold => might need to adjust after the first pass
                    if b1 != b2:
                        print("[%s] Wrong base threshold: %s. Find wrong match with threshold (score): %s" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), threshold, score))
                        error = True

                # Display file if error
                if error:
                    brand_and_f = utils.get_filename_we_and_f(path)
                    print("[%s] %d. %s : %.3f" % (str(datetime.now().strftime("%d-%m-%Y %H:%M")), j + 1, brand_and_f, score))
                    error = False
            print("\n")
