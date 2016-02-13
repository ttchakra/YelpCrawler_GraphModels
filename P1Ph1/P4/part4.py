import OrderedSet, re
import networkx as nx
import snap


def get_edge_count(edgelist_file):
    f = open(edgelist_file, 'r')
    lines = f.read().splitlines()
    e_len = len(lines)
    f.close()
    return e_len


def get_node_list(edgelist_file):
    node_list = OrderedSet.OrderedSet()
    f = open(edgelist_file, 'r')
    lines = f.read().splitlines()
    e_len = len(lines)
    for l in lines:
        m = re.search(r'(.+),(.+)', l)
        node_list.add(m.group(1))
        node_list.add(m.group(2))
    f.close()
    return node_list


def find_person(ordered_list, name):
    i = 0
    for el in ordered_list:
        if el == name:
            return i
        i += 1


def anonymize_names(edgelist_file, out_file):
    n = get_node_list(edgelist_file)
    f = open(edgelist_file, 'r')
    f1 = open(out_file, 'w')
    lines = f.read().splitlines()
    for l in lines:
        m = re.search(r'(.+),(.+)', l)
        name1 = m.group(1)
        name2 = m.group(2)
        aname1 = str(find_person(n, name1) + 1)
        aname2 = str(find_person(n, name2) + 1)
        f1.write(aname1 + "," + aname2 + '\n')
    f.close()
    f1.close()


def save_mapper_file(o, out_filename):
    f = open(out_filename, 'w')
    for i, el in enumerate(o):
        f.write(str(i+1) + "," + el + "\n")
    f.close()


def create_graph(edge_list_file, is_directed=True):
    edges = get_edges(edge_list_file)
    return create_graph_from_edges(edges, is_directed)


def create_graph_from_edges(edges, is_directed):
    if is_directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_edges_from(edges)
    return G


def get_edges(edge_list_file):
    f = open(edge_list_file, 'r')
    lines = f.read().splitlines()
    edges = []
    for l in lines:
        edges.append(tuple(l.split(',')))
    f.close()
    return edges


def get_degree_counts(G, nodes):
    """
    Compute number of nodes for each in-degree
    :param G: Network X Graph
    :param nodes: list of nodes for which you want aggregated counts
    :return: [(1, 10), (100, 3)] => [(indegree, count), ...]
    """
    degrees = G.in_degree(nodes)     # {0: 5, 1: 6, 2: 5}
    in_result = get_aggr_degree(degrees)
    degrees = G.out_degree(nodes)     # {0: 5, 1: 6, 2: 5}
    out_result = get_aggr_degree(degrees)
    return [in_result, out_result]


def get_aggr_degree(degrees):
    in_result = {}
    for k, v in degrees.items():
        if v in in_result:
            in_result[v] += 1
        else:
            in_result[v] = 1
    return in_result  # {5: 2, 6: 1}


def create_graph_for_snap(nodes, edge_list_file):
    edges = get_edges(edge_list_file)

    G = snap.TUNGraph.New()
    for n in nodes:
        G.AddNode(int(n))

    for e in edges:
        n1 = int(e[0])
        n2 = int(e[1])
        G.AddEdge(n1, n2)
    return G


def remove_x_percent_edges(x, edges):
    remaining_edges = len(edges) - int(x * len(edges))
    new_edge_list = []
    selected_indices = []
    import random
    while len(selected_indices) != remaining_edges:
        index_to_inc = int(random.random() * len(edges))
        print(index_to_inc)
        if index_to_inc not in selected_indices:
            new_edge_list.append(edges[index_to_inc])
            selected_indices.append(index_to_inc)
    return new_edge_list


def graph_size(G):
    return len(G.node)


def diameter_phase_transition():
    size_percent = []
    percents = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for x in percents:
        e = remove_x_percent_edges(x, get_edges('AnOutput.txt'))
        Gcc = sorted(nx.connected_component_subgraphs(create_graph_from_edges(e, False)), key=len, reverse=True)
        if len(Gcc) == 0:
            size_percent.append((x, 0))
        else:
            size_percent.append((x, graph_size(Gcc[0])))
    return size_percent


def key_with_max_val(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]



def get_out_degrees(G):
    return G.degree().values()

def main():
    # n = get_node_list('Output.txt')
    # save_mapper_file(n, 'Mapper.txt')
    # anonymize_names("Output.txt", 'AnOutput.txt')
    # an = get_node_list('AnOutput.txt')

    # G = create_graph('AnOutput.txt', True)
    # in_deg_res, out_deg_res = get_degree_counts(G, an)
    # print(in_deg_res, out_deg_res)
    # G1 = create_graph_for_snap(an, 'AnOutput.txt')

    # snap_traids = snap.GetTriads(G1)
    # triads = nx.transitivity(G)
    # pagerank = nx.pagerank(G)
    # max_pagerank = key_with_max_val(pagerank)
    # print max_pagerank
    # centrality = nx.in_degree_centrality(G)
    # eigen_vector_centrality = nx.eigenvector_centrality(G)
    # snap_dia = snap.GetBfsFullDiam(G1, 10)
    # dia = nx.diameter(G)
    # avg_local_clustering_coeff = nx.average_clustering(G)
    # global_clustering_coeff = snap.GetClustCf(G1, -1)
    # plot_data = diameter_phase_transition()

    n_len = 39892
    #print n_len
    e_len = 70942
    #print

    #random graph degree distribution
    G_random = nx.gnm_random_graph(n_len, e_len)
    an = G_random.node.keys()
    out_deg_res_rand = get_out_degrees(G_random)
    print(out_deg_res_rand)

    #preferential graph degree distribution
    G_pref = nx.barabasi_albert_graph(n_len, 4)
    an = G_pref.node.keys()
    out_deg_res_pref = get_out_degrees(G_pref)
    print(out_deg_res_pref)

    # small world graph degree distribution
    G_small = nx.fast_gnp_random_graph(n_len, 0.1)
    # an = G_small.node.keys()
    out_deg_res_small = get_out_degrees(G_small)
    print(out_deg_res_small)

    pass


if __name__ == '__main__':
    main()
