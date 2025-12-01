import pickle
import configparser
import logging
import os

import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

config_file = os.environ['CONFIG']
config = configparser.ConfigParser()
config.read(config_file)
logging.basicConfig(level=config.get('DEFAULT', 'log_level'))
log = logging.getLogger(os.path.basename(__file__))

def robustness_analysis(G, strategy='targeted'):
    """
    Performs a robustness analysis by removing nodes and tracking the size of the largest connected component.

    :param G: The graph to analyze.
    :param strategy: 'targeted' (removes nodes by decreasing betweenness centrality) or 'random'.
    :return: A list with the size of the largest connected component after each node removal.
    """
    g_copy = G.copy()
    lcc_sizes = []

    if strategy == 'targeted':
        # Calcula uma vez betweenness centrality
        nodes_to_remove = sorted(nx.betweenness_centrality(g_copy).items(), key=lambda item: item[1], reverse=True)
        nodes_to_remove = [node for node, centrality in nodes_to_remove]
    elif strategy == 'random':
        nodes_to_remove = list(g_copy.nodes())
        np.random.shuffle(nodes_to_remove)
    else:
        raise ValueError("A estrategia deve ser 'targeted' ou 'random'")

    for node in nodes_to_remove:
        g_copy.remove_node(node)
        if g_copy.number_of_nodes() > 0:
            largest_cc = max(nx.connected_components(g_copy), key=len)
            lcc_sizes.append(len(largest_cc))
        else:
            lcc_sizes.append(0)
    return lcc_sizes


if __name__ == "__main__":
    with open("../../data/graph_50.gpickle", 'rb') as f:
        G1 = pickle.load(f)
        # Calcular o grau de cada nó
        degrees = [d for _, d in G1.degree()]
        mean_degree = np.mean(degrees)
        log.info(f"Mean degree: {mean_degree:.4f}")

        # Contar quantos nós têm cada grau
        degree_counts = {}
        for d in degrees:
            degree_counts[d] = degree_counts.get(d, 0) + 1

        # Ordenar os graus
        sorted_degrees = sorted(degree_counts.items())

        # Separar os eixos
        x, y = zip(*sorted_degrees)

        # 5 Plotar a distribuição de graus
        plt.figure(figsize=(8, 5))
        plt.bar(x, y, width=0.8, color='skyblue', edgecolor='black')
        plt.title("Degree Distribution")
        plt.xlabel("Degree (k)")
        plt.ylabel("Number of Nodes")
        plt.axvline(mean_degree, label='<k>', color='blue')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.savefig(f"../../data/degree_distribution.png", bbox_inches="tight")

        plt.figure(figsize=(8, 5))
        plt.scatter(x,np.array(y)/G1.number_of_nodes(), color='skyblue')
        plt.axvline(mean_degree, label='<k>', color='blue')
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.title("Degree Probability (log-log scale)")
        plt.xlabel("Degree (k)")
        plt.ylabel("P(k)")
        plt.grid(alpha=0.3)
        plt.savefig(f"../../data/degree_distribution_log_log.png", bbox_inches="tight")

        # 2. Mean Distance (Distância Média)
        # Verifica se o grafo é conectado
        if nx.is_connected(G1):
            mean_distance = nx.average_shortest_path_length(G1)
            log.info(f"Mean Distance: {mean_distance:.2f}")
        else:
            # Se não for conectado, calcula para o maior componente
            largest_cc = max(nx.connected_components(G1), key=len)
            G_largest = G1.subgraph(largest_cc).copy()
            mean_distance = nx.average_shortest_path_length(G_largest, weight="weight")
            log.info(f"Mean Distance (largest component): {mean_distance:.2f}")
            log.info(f"  Note: Graph has {nx.number_connected_components(G1)} components")

        # 3. Clustering Coefficient (Coeficiente de Agrupamento)
        clustering_coeff = nx.average_clustering(G1)
        log.info(f"Clustering Coefficient: {clustering_coeff:.4f}")

        # Distribuição de Clustering Coefficient local
        plt.figure(figsize=(8, 5))
        local_clustering = nx.clustering(G1)
        clustering_values = list(local_clustering.values())
        plt.hist(clustering_values, bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
        plt.axvline(clustering_coeff, color='red', linestyle='--', linewidth=2,
                    label=f'Mean: {clustering_coeff:.4f}')
        plt.title("Local Clustering Coefficient Distribution")
        plt.xlabel("Clustering Coefficient")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.savefig(f"../../data/clustering_distribution.png", bbox_inches="tight")

        # 4. Betweenness Centrality (Centralidade de Intermediação)
        betweenness = nx.betweenness_centrality(G1)
        mean_betweenness = np.mean(list(betweenness.values()))
        log.info(f"Mean Betweenness Centrality: {mean_betweenness:.6f}")
        log.info("=" * 50)

        # Distribuição de Betweenness Centrality
        plt.figure(figsize=(10, 5))
        betweenness_values = sorted(betweenness.values(), reverse=True)
        plt.plot(betweenness_values, linewidth=2, color='coral')
        plt.title("Betweenness Centrality Distribution")
        plt.xlabel("Node Rank")
        plt.ylabel("Betweenness Centrality")
        plt.grid(alpha=0.3)
        plt.savefig(f"../../data/betweenness_distribution.png", bbox_inches="tight")

        # Top 10 nós com maior Betweenness
        plt.figure(figsize=(10, 6))
        top_10_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
        nodes, values = zip(*top_10_nodes)
        plt.barh(range(len(nodes)), values, color='lightcoral', edgecolor='black')
        plt.yticks(range(len(nodes)), [f"Node {n}" for n in nodes])
        plt.xlabel("Betweenness Centrality")
        plt.title("Top 10 Nodes by Betweenness Centrality")
        plt.grid(alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig(f"../../data/top_betweenness_nodes.png", bbox_inches="tight")

        # 5. Análise de Robustez
        log.info("Starting robustness analysis...")

        # Ataque direcionado baseado na centralidade de intermediação
        lcc_targeted = robustness_analysis(G1, strategy='targeted')

        # Falha aleatória
        lcc_random = robustness_analysis(G1, strategy='random')

        # Plotando os resultados
        plt.figure(figsize=(10, 6))
        num_nodes = G1.number_of_nodes()
        fraction_removed = np.linspace(0, 1, num_nodes)

        plt.plot(fraction_removed, np.array(lcc_targeted) / num_nodes, '#ff7966ff', label='Targeted Attack (by Betweenness)')
        plt.plot(fraction_removed, np.array(lcc_random) / num_nodes, '#f5b073ff', label='Random Failure')

        plt.title("Graph Robustness to Node Removal")
        plt.xlabel("Fraction of Nodes Removed")
        plt.ylabel("Fractional Size of Largest Connected Component")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.savefig(f"../../data/robustness_analysis.png", bbox_inches="tight")
        log.info("Robustness analysis finished. Plot saved to ../../data/robustness_analysis.png")


