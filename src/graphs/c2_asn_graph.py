import db
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

G = nx.Graph()

print("Getting C2 GeoData")
p2p_nodes = db.IpGeoData.objects(server_type="C2 Server").all()

print(len(p2p_nodes), "C2s pulled")
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
    G.add_node(node, fillcolor='mediumseagreen')
    G.add_edge(asn, node)

print("Drawing graph")

counter_asn = Counter(asn_counts)
print("Top 10 most common ASNs", counter_asn.most_common(10))

colored_dict = nx.get_node_attributes(G, 'fillcolor')
d = dict(G.degree)

nx.draw(G,
    edge_color='lightgrey',
    node_color=[colored_dict.get(node, 'mediumseagreen') for node in G.nodes()],
    pos = nx.spring_layout(G, k=0.03, iterations=50),
    labels={k: f'ASN {k}' if v > 5 else '' for k,v in d.items()},
    font_size=13,
    node_size=3,
    font_color="blue",
)

colors = ["red", "mediumseagreen"]
texts = ['ASN', 'Candidate C2 Servers']
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