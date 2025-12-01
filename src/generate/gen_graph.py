import configparser
import logging
import os

import networkx as nx
import numpy as np
import pandas as pd
from haversine import haversine, Unit, haversine_vector
from statistics import mean
import pickle

from tqdm import tqdm

config_file = os.environ['CONFIG']
config = configparser.ConfigParser()
config.read(config_file)
logging.basicConfig(level=config.get('DEFAULT', 'log_level'))
log = logging.getLogger(os.path.basename(__file__))

'''
Subtask:
Define a method to add edges between nodes based on a distance metric or other criteria.

Reasoning: Define a function to calculate geographical distance between two nodes and then iterate through all node pairs to add edges based on a distance threshold. I will use the haversine library for distance calculation.
'''
def add_edges_by_distance(graph, distance_threshold=10): # Distance in kilometers
    """Adds edges to a graph based on geographical distance between nodes."""
    nodes = list(graph.nodes(data=True))
    for i in tqdm(range(len(nodes)), desc="Add edges", total=len(nodes), unit="nodes"):
        for j in range(i + 1, len(nodes)):
            node1_index, node1_data = nodes[i]
            node2_index, node2_data = nodes[j]

            lat1 = node1_data['Latitude']
            lon1 = node1_data['Longitude']
            lat2 = node2_data['Latitude']
            lon2 = node2_data['Longitude']

            distance = haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)

            if distance < distance_threshold:
                graph.add_edge(node1_index, node2_index, weight=distance)

def merge_close_nodes(graph, distance_threshold=1):
    """Merges close nodes in a graph based on geographical distance."""
    nodes_to_merge = set()
    merged_nodes = {}

    nodes = list(graph.nodes(data=True))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1_index, node1_data = nodes[i]
            node2_index, node2_data = nodes[j]

            lat1 = node1_data['Latitude']
            lon1 = node1_data['Longitude']
            lat2 = node2_data['Latitude']
            lon2 = node2_data['Longitude']

            distance = haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)

            if distance < distance_threshold:
                # find if indexes are already in some list
                for key, values in merged_nodes.items():
                    if node1_index in values and node2_index not in values:
                        merged_nodes[key].append(node2_index)
                        nodes_to_merge.add(node2_index)
                        break;
                    if node1_index not in values and node2_index in values:
                        merged_nodes[key].append(node1_index)
                        nodes_to_merge.add(node1_index)
                        break;
                else:
                # Merge node2 into node1
                    merged_nodes[node1_index] = [node1_index]
                    merged_nodes[node1_index].append(node2_index)
                    nodes_to_merge.add(node2_index)

    # Create a new graph with merged nodes
    H = nx.Graph()
    for node_index, node_data in tqdm(graph.nodes(data=True), desc="Merge step 2", total=len(graph.nodes), unit="nodes"):
        if node_index not in nodes_to_merge:
          if node_index in merged_nodes:
            lats = []
            longs = []
            frp = []
            for original_node in merged_nodes[node_index]:
                lats.append(graph.nodes[original_node]['Latitude'])
                longs.append(graph.nodes[original_node]['Longitude'])
                frp.append(graph.nodes[original_node]['FRP'])
            #log.info(f"merged {len(frp)} into one node; lats = {lats} mean={mean(lats)}")
            H.add_node(node_index, Latitude=mean(lats), Longitude=mean(longs), FRP=sum(frp))
          else:
            H.add_node(node_index, **node_data)

    # Add edges to the new graph
    for edge in tqdm(graph.edges(data=True), desc="Merge step 3", total=len(graph.edges), unit="edges"):
        u, v, data = edge
        if u not in nodes_to_merge and v not in nodes_to_merge:
            H.add_edge(u, v, **data)
        elif u in merged_nodes and v not in nodes_to_merge:
            for original_node in merged_nodes[u]:
                if graph.has_edge(original_node, v):
                     H.add_edge(u, v, **graph.get_edge_data(original_node, v))
        elif v in merged_nodes and u not in nodes_to_merge:
             for original_node in merged_nodes[v]:
                if graph.has_edge(u, original_node):
                     H.add_edge(u, v, **graph.get_edge_data(u, original_node))
        elif u in merged_nodes and v in merged_nodes and u != v:
             for original_node_u in merged_nodes[u]:
                 for original_node_v in merged_nodes[v]:
                     if graph.has_edge(original_node_u, original_node_v):
                         H.add_edge(u, v, **graph.get_edge_data(original_node_u, original_node_v))

    return H


if __name__ == "__main__":
    csv_file = '../../data/queimadas.csv'

    df = pd.read_csv(csv_file)
    G = nx.Graph()

    '''
    Subtask:
    Add nodes to the graph using the 'Latitude' and 'Longitude' columns from the df DataFrame.
    
    Reasoning: Iterate through the dataframe and add nodes with latitude and longitude attributes to the graph.
    '''
    for index, row in df.iterrows():
        G.add_node(index, Latitude=row['Latitude'], Longitude=row['Longitude'], FRP=row["FRP"])

    merge_distance = config.getint("generate", "merge_distance", fallback=1)
    G = merge_close_nodes(G, merge_distance)  # 1km default
    log.info(f"merge distance = {merge_distance}")
    add_edges_distance = config.getint("generate", "add_edges_distance", fallback=10)
    log.info(f"add edges distance = {add_edges_distance}")
    add_edges_by_distance(G, add_edges_distance)  # 10 km default

    log.info(f"edges = {G.number_of_edges()}")
    log.info(f"nodes = {G.number_of_nodes()}")
    log.info(f"components = {nx.number_connected_components(G)}")
    with open("../../data/graph_1_10.gpickle", 'wb') as f:
        pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)