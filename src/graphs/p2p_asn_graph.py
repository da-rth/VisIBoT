import db
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

G = nx.Graph()

print("Getting P2P GeoData")
p2p_nodes = db.IpGeoData.objects(server_type="P2P Node").all()

print(len(p2p_nodes), "P2P nodes pulled")
print("Generating Graph...")

asn_counts = {}

for node in p2p_nodes:
    asn = node.asn.asn
    node = node.ip_address

    if asn not in asn_counts:
        asn_counts[asn] = 1
    else:
        asn_counts[asn] += 1

    G.add_node(asn, fillcolor='red')
    G.add_node(node, fillcolor='lightblue')
    G.add_edge(asn, node)

print("Drawing graph")

counter_asn = Counter(asn_counts)
print("Top 10 most common ASNs", counter_asn.most_common(10))

colored_dict = nx.get_node_attributes(G, 'fillcolor')
d = dict(G.degree)

nx.draw(G,
    edge_color='lightgrey',
    node_color=[colored_dict.get(node, 'lightblue') for node in G.nodes()],
    pos = nx.spring_layout(G, k=0.03, iterations=50),
    labels={k: f'ASN {k}' if v > 40 else '' for k,v in d.items()},
    font_size=13,
    node_size=3,
    font_color="blue",
)

colors = ["red", "lightblue"]
texts = ['ASN', 'P2P Nodes']
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

# plt.savefig("ConnectionsGraph.png", format="PNG", dpi=1200)
# print("Saved graph to ConnectionsGraph.png")