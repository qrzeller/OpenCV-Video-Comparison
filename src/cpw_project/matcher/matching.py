from matcher import ssim
from matcher import orb
import networkx as nx
from datetime import datetime
from networkx import readwrite
import utils
import cv2
import json


def matching(scenes_path, matcher_type, result_json_match_path, result_txt_match_path):

    # Graf to process match
    G = nx.MultiGraph()

    # Load image path as matrix
    images = load_images(scenes_path)

    # Get the number of iteration to match all images
    maximum = get_max_iter(scenes_path)

    # Process all images in scene directory
    matches = 0
    progress = 0
    removed = []
    for k_base, v_base in images.items():
        if not [s for s in removed if k_base in s]:
            for k_compare, v_compare in images.items():
                if not [s for s in removed if k_compare in s]:
                    if k_base != k_compare:
                        for i_base in v_base:
                            for i_compare in v_compare:
                                if matcher_type == "orb":
                                    match = orb.detect_match(i_base, i_compare)
                                    if len(match) > 0:
                                        G.add_edge(k_base, k_compare, weight=len(match))
                                        matches = matches + 1
                                if matcher_type == "ssim":
                                    match, score = ssim.detect_match(i_base, i_compare)
                                    if match:
                                        G.add_edge(k_base, k_compare, weight=score)
                                        matches = matches + 1
                                progress = progress + 1
            print("[%s] Current process: %s/%s; Match on video: %s" % (str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")), str(progress), str(maximum), str(matches)))
            matches = 0
            removed.append(k_base)

    # Save graph relation
    nx.write_edgelist(G, result_txt_match_path)
    with open(result_json_match_path, 'w') as f:
        f.write(json.dumps(readwrite.json_graph.node_link_data(G)))


# Load image matrix from image path
def load_images(scenes_path):
    directories = utils.get_all_directories(scenes_path)
    images = {}
    for directory in directories:
        files = utils.get_all_files(directory)
        for file in files:

            # Check if not black nor white image
            if not utils.remove_white_black_image(file.path):
                images.setdefault(utils.get_video_name(directory), []).append(cv2.imread(file.path, 0))
    return images


def get_max_iter(scenes_path):
    directories = utils.get_all_directories(scenes_path)
    i = 0
    for d_base in directories:
        files_base = utils.get_all_files(d_base)
        for d_compare in directories:
            files_compare = utils.get_all_files(d_compare)
            # Check to not compare same directory
            if d_base != d_compare:
                for fb in files_base:
                    for fc in files_compare:
                        i = i + 1
        directories.remove(d_base)
    return i