import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

G = nx.Graph()
c2asn_df = pd.read_csv('ip_asn.csv')
c2_asn_hist = {}

for i, c2_asn in c2asn_df.iterrows():
    c2_ip = c2_asn['ip_address']
    maintainer = c2_asn['maintainer']

    if c2_ip not in c2_asn_hist:
        c2_asn_hist[c2_ip] = [maintainer]
    else:
        c2_asn_hist[c2_ip].append(maintainer)

    G.add_node(maintainer, fillcolor='red')
    G.add_node(c2_ip, fillcolor='mediumseagreen')
    G.add_edge(maintainer, c2_ip)

colored_dict = nx.get_node_attributes(G, 'fillcolor')
d = dict(G.degree)

nx.draw(G,
    edge_color='lightgrey',
    node_color=[colored_dict.get(node, 'mediumseagreen') for node in G.nodes()],
    pos=nx.spring_layout(G, k=0.03, iterations=50),
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
