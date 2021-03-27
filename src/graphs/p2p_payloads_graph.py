import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
G = nx.Graph()

payloads_df = pd.read_csv('p2p_payloads.csv')
source_conns = []
dest_conns = []
dest_edges = {}

for payload in payloads_df.iterrows():
    source_ip = payload['ip_address']
    source_conns.append(source_ip)

    for dest_ip in payload['candidate_P2Ps']:
        if dest_ip not in dest_edges:
            dest_edges[dest_ip] = []

        dest_conns.append(dest_ip)
        dest_edges[dest_ip].append(source_ip)

G.add_nodes_from(source_conns, fillcolor='red', node_size=30)
G.add_nodes_from(dest_conns, fillcolor='blue', node_size=5)

def zip_with_scalar(l, o):
    return ((i, o) for i in l)

for dest_ip, conns in dest_edges.items():
    conn_edges = zip_with_scalar(conns, dest_ip)
    G.add_edges_from(conn_edges)

colored_dict = nx.get_node_attributes(G, 'fillcolor')
color_seq = [colored_dict.get(node, 'blue') for node in G.nodes()]

nx.draw(
    G,
    with_labels=False,
    node_size=[v^5 for v in dict(G.degree).values()],
    edge_color='lightgrey',
    node_color=color_seq
)

colors = ["red", "blue"]
texts = ['Malware Binaries', 'P2P Nodes']
patches = [
    plt.plot(
        [],
        [],
        marker="o",
        ms=10,
        ls="",
        mec=None,
        color=colors[i], 
        label="{:s}".format(texts[i])
    )[0] for i in range(len(texts))
]

plt.legend(handles=patches)
plt.title("This is a title")
plt.show()
