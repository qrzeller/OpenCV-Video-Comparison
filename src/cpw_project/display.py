import matplotlib.pyplot as plt
import networkx as nx
import utils
import json
import os
import re


def get_video_path_by_name(name, videos_path):

    # Get all videos files
    files = utils.get_all_files(videos_path)
    for file in files:

        # Check if the video is the same as the name
        if utils.get_video_name(file) == name:
            return file
    return ""


def gen_video_id(result_js_db_path, datas, videos_path):
    group = 0
    for k, v in datas.items():
        write_data(result_js_db_path, '{"id":"' + k + '"},\n')
        # ,
        # Get video path by video name
        #video_path = get_video_path_by_name(k, videos_path).path
        ##v = video_path.replace("\\", "\\\\")
        ##node = str('{id:"' + k + '", title:' + '\'' + '<strong>Video path:</strong> ' + v + '<br><br><video width="400" controls><source src="' + v + '" type="video/mpg">Your browser does not support HTML5 video.</video>' + '\'' + ', group:' + str(group) + '},\n')
        ##write_data(result_js_db_path, node)
        group = group + 1


def gen_photo_id(result_js_db_path, datas):
    group = 0
    node_id = 0
    for k, v in datas.items():
        for file in v:
            write_data(result_js_db_path, '{"id":"' + str(node_id) + '"},\n')
            ##f = file.replace("\\", "\\\\")
            ##node = str('{id:' + str(node_id) + ', title:' + '\'' + '<strong>Image path:</strong> ' + f + '<br><br><img src="' + f + '" width="500" height="377">' + '\'' + ', group:' + str(group) + '},\n')
            ##write_data(result_js_db_path, node)
            node_id = node_id + 1
        group = group + 1


def write_data(result_js_db_path, data):
    with open(result_js_db_path, "a+") as f:
        f.write(data)


def gen_nodes(datas, result_js_db_path, videos_path):
    ##write_data(result_js_db_path, "var nodes = [\n")
    gen_video_id(result_js_db_path, datas, videos_path)
    gen_photo_id(result_js_db_path, datas)
    ##write_data(result_js_db_path, "]")


def gen_edges(datas, result_js_db_path):
    ##write_data(result_js_db_path, "var edges = [\n")
    node_id = 0
    for k, v in datas.items():
        for file in v:
            write_data(result_js_db_path, '{"source": "' + str(node_id) + '", "target": "' + k + '"},\n')
            #write_data(result_js_db_path, '{from: ' + str(node_id) + ', to: "' + k + '"},\n')
            node_id = node_id + 1
    ##write_data(result_js_db_path, "]")


def gen_database_js(result_json_path, result_js_db_path, videos_path):

    # Load result
    with open(result_json_path) as j:
        datas = json.load(j)

    write_data(result_js_db_path, '{\n')
    write_data(result_js_db_path, '"type": "NetworkGraph",\n')
    write_data(result_js_db_path, '"label": "Ninux Roma",\n')
    write_data(result_js_db_path, '"protocol": "OLSR",\n')
    write_data(result_js_db_path, '"version": "0.6.6.2",\n')
    write_data(result_js_db_path, '"metric": "ETX",\n')
    write_data(result_js_db_path, '"nodes": [\n')

    # Gen all nodes in js file
    gen_nodes(datas, result_js_db_path, videos_path)

    write_data(result_js_db_path, '],\n')
    write_data(result_js_db_path, '"links": [\n')

    # Gen all edges in js file
    gen_edges(datas, result_js_db_path)

    write_data(result_js_db_path, ']\n')
    write_data(result_js_db_path, '}\n')




def display_graph(result_json_file):

    # Load result
    with open(result_json_file) as js:
        datas = json.load(js)

    # Add data as edge
    G = nx.Graph()
    for k, v in datas.items():
        for c in v:
            G.add_edge(k, utils.get_video_name(c))

    # Plot the graph
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()