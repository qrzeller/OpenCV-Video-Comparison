import index
import search
from datetime import datetime


def main():

    # Time start
    t0 = datetime.now()

    project_path = "C:\\Users\\Admin\\Documents\\GitHub\\opencv_video_comparison\\src\\custom_video_classifier\\"
    image_path = project_path + "images\\"
    index_path = project_path + "index.pickle"

    #index.index_images(image_path, index_path)
    search.search_match(index_path)

    # Get time and compare
    t1 = datetime.now()
    print("Duration: %s" % (t1 - t0))


if __name__ == "__main__":
    main()