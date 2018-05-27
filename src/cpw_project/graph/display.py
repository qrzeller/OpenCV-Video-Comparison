import networkx as nx
import matplotlib.pyplot as plt
import community

from graph import reparser


def find_clusters(G):
    cliques = nx.algorithms.find_cliques(G)
    tot = 0
    moyenne = 0
    max_len = 0
    for i in cliques:
        if len(i) >= 2:
            print(i)
            tot+=1
        count = 0
        for j in i:
            count += 1
        moyenne += count
        if count > max_len:
            max_len = count

    print("Nombre de cliques" + str(tot))








    print("taille moyenne des cliques : " + str(moyenne / tot))
    print("longueur maximale d'une clique : " + str(max_len))

    return cliques

def connected_component(G):
    con_comp = nx.algorithms.connected_components(G)
    for i in con_comp:
        print(i)


def all_cliques(G):
    return nx.algorithms.enumerate_all_cliques(G)


def community_by_louvain(G,with_labels):
    plt.figure(figsize=(25, 12), dpi=150)

    partition = community.best_partition(G)

    # drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=60,
                               node_color=str(count / size),label=True)

    nx.draw_networkx_edges(G, pos, alpha=0.4)
    if with_labels:
        nx.draw_networkx_labels(G, pos)
    plt.show()

def read_adj(with_labels=True, plot=True):
    path = "../datas/result_orb.txt"

#    reparser.reparse_file(path)
#    path = "../datas/video_graph/ssim_v.txt"

    G = nx.read_edgelist(path,create_using=nx.MultiGraph())


    print("Finished reading graph: " + path.split("/")[2])


    """
    it = G.edges(data=True, keys=True)
    for i in it:
        print(i)
        if i[2]['weight'] > 0.9:
            G.remove_edge(i[0],i[1])
    """



    cliques = find_clusters(G)
    #connected_component(G)
    community_by_louvain(G,with_labels)




    if plot:
        # Display with different color relative to edge weight
        pos = nx.spring_layout(G)
        edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
        nx.draw(G, pos, node_color='#A0CBE2', edgelist=edges, edge_color=weights,
                width=4, edge_cmap=plt.cm.Blues)
        if with_labels:
            nx.draw_networkx_labels(G, pos, font_size=6)

        # Default basic display
        # nx.draw(G, with_labels=with_labels)

        plt.show()




read_adj(plot=False,with_labels=False)
