import db
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

print("Getting Payload Data")
payloads = db.MalwarePayload.objects(candidate_P2Ps__exists=True, candidate_P2Ps__not__size=0, keyword="mirai")

print(len(payloads), "payloads pulled")

source_conns = []
dest_conns = []
dest_edges = {}
sum_dests = 0
min_dests = len(payloads[0].candidate_P2Ps)
max_dests = len(payloads[0].candidate_P2Ps)

print("Generating Graph...")

for payload in payloads:
    source_ip = payload.ip_address.ip_address
    source_conns.append(source_ip)
    
    num_nodes = len(payload.candidate_P2Ps)
    
    if num_nodes > max_dests:
        max_dests = num_nodes
    
    if num_nodes < min_dests:
        min_dests = num_nodes

    for p in payload.candidate_P2Ps:
        sum_dests += 1
        dest_ip = p.ip_address

        if dest_ip not in dest_edges:
            dest_edges[dest_ip] = []

        dest_conns.append(dest_ip)
        dest_edges[dest_ip].append(source_ip)

G.add_nodes_from(source_conns, fillcolor='red', node_size=30)
G.add_nodes_from(dest_conns, fillcolor='blue', node_size=5)

avg_nodes = int(sum_dests / len(source_conns))
print(f"Payloads: {len(source_conns)} | P2P Nodes: {len(dest_conns)} | Min: {min_dests} | Max: {max_dests} | Avg: {avg_nodes}")

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

# plt.savefig("ConnectionsGraph.png", format="PNG", dpi=1200)
# print("Saved graph to ConnectionsGraph.png")