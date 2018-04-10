import os
import json
import re
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image


def remove_special_char(video_path):
    video_files = get_files(video_path)
    for file in video_files:
        file_dir = os.path.dirname(file)
        base = os.path.basename(file)
        name = os.path.splitext(base)[0]
        new_file = os.path.join(file_dir, ''.join(e for e in name if e.isalnum()) + os.path.splitext(base)[1])
        os.rename(file, new_file)


def get_file(path):
    name, ext = os.path.splitext(os.path.basename(path))
    return name, ext


def get_video_name(path):
    return get_filename_we(path).split('_')[0]


def get_filename_we(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_filename_we_and_nf(path):
    return (os.path.splitext(os.path.basename(path))[0]).split("_")[0]


def get_filename_we_and_f(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_brand(path):
    r = re.compile("([0-9]+)([a-zA-Z]+)([0-9]+)")
    m = r.match(path)
    return m.group(2)

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_files(directory):
    files = []
    for file in os.listdir(directory):
        files.append(os.path.join(directory, file))
    return files


def get_files_rec(directory):
    files = []
    for root, directories, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def save_json_match(dico_match, result_json_file):
    with open(result_json_file, 'w') as fp:
        json.dump(dico_match, fp)


def get_video_brand(video_name):
    r = re.compile("([0-9]+)([a-zA-Z]+)([0-9]+)")
    m = r.match(video_name)
    return m.group(2)#, m.group(2), m.group(3)


def display_graph(result_json_file):

    # Load result
    with open(result_json_file) as js:
        datas = json.load(js)

    # Add data as edge
    G = nx.Graph()
    for k, v in datas.items():
        for c in v:
            G.add_edge(k, get_video_name(c))

    # Plot the graph
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


def sort_video_ba_brand(directory, result_json_file):
    dico_match = {}
    files = os.listdir(directory)
    for dir in files:
        dico_match.setdefault(get_video_brand(dir), []).append(dir)
    save_json_match(dico_match, result_json_file)
    display_graph(result_json_file)


def remove_white_black_image(path):
    img = Image.open(path)
    if sum(img.convert("L").getextrema()) in (0, 2):
        return True
    return False


def gen_database_js(result_json_file, db_result_js_path):

    # Load result
    with open(result_json_file) as js:
        datas = json.load(js)


    for k, v in datas.items():
        for file in v:
            pass
