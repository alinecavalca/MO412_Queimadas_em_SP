import configparser
import logging
import os

import pickle
from statistics import mean
import networkx as nx
from gen_graph import add_edges_by_distance

config_file = os.environ['CONFIG']
config = configparser.ConfigParser()
config.read(config_file)

logging.basicConfig(level=config.get('DEFAULT', 'log_level'))
log = logging.getLogger(os.path.basename(__file__))

def create_subgraph_from_edges(G):

#If you only want the largest connected component, it’s more efficient to use max instead of sort.

  largest_cc = max(nx.connected_components(G), key=len)
  log.info(f"largest cc = {len(largest_cc)}")
  #To create the induced subgraph of each component, use:
  S = [G.subgraph(c).copy() for c in nx.connected_components(G)]

  H = nx.Graph()
  for sg in S:
    lats = []
    longs = []
    frp = []
    for node_index, node_data in sg.nodes(data=True):
        lats.append(node_data['Latitude'])
        longs.append(node_data['Longitude'])
        frp.append(node_data['FRP'])
    H.add_node(sg, Latitude=mean(lats), Longitude=mean(longs), FRP=sum(frp))

  return H

if __name__ == "__main__":
    with open("../../data/graph_1_10.gpickle", 'rb') as f:
        G = pickle.load(f)
        G1 = create_subgraph_from_edges(G)

        add_edges_distance = config.getint("generate", "add_edges_distance2", fallback=50)
        log.info(f"add edges distance = {add_edges_distance}")
        add_edges_by_distance(G1, add_edges_distance)  # 10 km default

        log.info(f"edges = {G1.number_of_edges()}")
        log.info(f"nodes = {G1.number_of_nodes()}")
        log.info(f"components = {nx.number_connected_components(G1)}")
        with open("../../data/graph_50.gpickle", 'wb') as f2:
            pickle.dump(G1, f2, pickle.HIGHEST_PROTOCOL)
