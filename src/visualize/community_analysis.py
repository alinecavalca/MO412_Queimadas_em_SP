import itertools
import configparser
import logging
import os
import pickle

import networkx as nx
from networkx.algorithms import community as nx_comm
#import networkx.community 
from matplotlib import pyplot as plt

from plot_graph import plot_communities

config_file = os.environ['CONFIG']
config = configparser.ConfigParser()
config.read(config_file)
logging.basicConfig(level=config.get('DEFAULT', 'log_level'))
log = logging.getLogger(os.path.basename(__file__))
GRAPH_FILE = "../../data/graph_50.gpickle"

if __name__ == "__main__":
    if not os.path.exists(GRAPH_FILE):
        log.error(f"Graph file not found at {GRAPH_FILE}")
        exit(1)

    with open(GRAPH_FILE, 'rb') as f:
        G = pickle.load(f)

    log.info("Starting community detection using Louvain algorithm...")

    # Detectar comunidades usando o algoritmo de Louvain
    communities = nx_comm.louvain_communities(G, weight='weight', seed=42)
    log.info(f"Found {len(communities)} communities.")

    # Criar um mapeamento de nó para ID da comunidade para colorir
    node_to_community = {}
    for i, community in enumerate(communities):
        for node in community:
            node_to_community[node] = i

    # Gerar uma lista de cores para as comunidades
    # Usamos um ciclo de cores para o caso de haver muitas comunidades
    color_cycle = itertools.cycle(plt.cm.get_cmap('tab20').colors)
    community_colors = [next(color_cycle) for _ in range(len(communities))]

    # Mapear a cor para cada nó
    node_colors = [community_colors[node_to_community[node]] for node in G.nodes()]

    log.info("Plotting graph with detected communities...")
    plot_communities(G, node_colors, title="Fire Spot Communities (Louvain)")
