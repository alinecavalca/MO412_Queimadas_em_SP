'''
Visualize or analyze
Subtask:
Provide options for visualizing or analyzing the created network.
'''
import configparser
import logging
import os
import pickle
import re
from statistics import quantiles

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

config_file = os.environ['CONFIG']
config = configparser.ConfigParser()
config.read(config_file)
logging.basicConfig(level=config.get('DEFAULT', 'log_level'))
log = logging.getLogger(os.path.basename(__file__))

def plot(graph, title="Network based on Latitude and Longitude", img_src=None):
  # Create a dictionary of positions for the nodes using Latitude and Longitude
  pos = {node: (data['Longitude'], data['Latitude']) for node, data in graph.nodes(data=True)}

  frp = np.array(list(data for node, data in graph.nodes(data="FRP")))
  log.info(f"min frp = {min(frp)}")
  log.info(f"max frp = {max(frp)}")
  sizes = frp - min(frp) + 1 # min size 1
  sizes = np.emath.power(sizes, 3/4 ) # max size is sizes**(3/4)
  log.info(f"min sizes = {min(sizes)}")
  log.info(f"max sizes = {max(sizes)}")

  # Draw the network
  fig, ax = plt.subplots(figsize=(18, 12))
  longs = [p[0] for p in pos.values()]
  lats = [p[1] for p in pos.values()]
  log.info(f"min long = {min(longs)}")
  log.info(f"max long = {max(longs)}")
  log.info(f"min lat = {min(lats)}")
  log.info(f"max lat = {max(lats)}")
  if img_src:
      img = plt.imread(img_src)
      ax.imshow(img, extent=[-53.2, max(longs), -25.2, max(lats)])
  nx.draw(graph, pos, with_labels=False, node_size=sizes, edge_color='#27211e', alpha=0.6, node_color='#ff7966')
  plt.title(title, fontsize=20)
  plt.xlabel("Longitude")
  plt.ylabel("Latitude")

  # Create dummy scatter plots for the legend
  # The 's' parameter in scatter corresponds to the area, so you might need to adjust for visual representation
  # If your node_size in nx.draw is proportional to radius, then s should be proportional to radius^2
  n = 1000
  quantiles_pack = list(zip(quantiles(frp, n=n), quantiles(sizes, n=n)))
  for i in range(0, n, n//10-1):
    frp,size = quantiles_pack[i]
    plt.scatter([], [], s=size, color='#ffbcb3', label=f'{frp:.0f}')

  plt.legend(scatterpoints=1, frameon=False, labelspacing=2, reverse=True, title='FRP')
  title = re.sub(r'[^\x00-\x7F]+', '', title)
  title = title.replace(" ", "_")
  #plt.show()
  plt.savefig(f"../../data/{title}.png", bbox_inches="tight")

if __name__ == "__main__":
    with open("../../data/graph_1_10.gpickle", 'rb') as f:
        G = pickle.load(f)
        add_edges_distance = config.getint("generate", "add_edges_distance", fallback=10)
        plot(G, f"{add_edges_distance} km de distância")
        plot(G, f"{add_edges_distance} km de distância sobre Transporte", "Mapa_de_transportes_em_São_Paulo.jpg")
        plot(G, f"{add_edges_distance} km de distância sobre Densidade Populacional", "SP_DensidadePopulacional.png")

    with open("../../data/graph_50.gpickle", 'rb') as f:
        G1 = pickle.load(f)
        add_edges_distance = config.getint("generate", "add_edges_distance2", fallback=50)
        plot(G1, f"{add_edges_distance} km de distância")
        plot(G1, f"{add_edges_distance} km de distância sobre Transporte", "Mapa_de_transportes_em_São_Paulo.jpg")
        plot(G1, f"{add_edges_distance} km de distância sobre Densidade Populacional", "SP_DensidadePopulacional.png")