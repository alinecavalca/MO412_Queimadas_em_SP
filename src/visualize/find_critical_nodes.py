import configparser
import logging
import os
import pickle

import EoN
import networkx as nx
from matplotlib import pyplot as plt
from tqdm import tqdm

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

    # --- 1. SIMULAÇÃO PARA ENCONTRAR NÓS CRÍTICOS ---
    log.info("Starting simulations to find most dangerous ignition points...")

    # Parâmetros da simulação. Usamos um tau alto (pior cenário) para
    # revelar melhor as vulnerabilidades da rede.
    tau = 1.0
    gamma = 1.0

    fire_outbreak_sizes = {}

    # Usamos tqdm para mostrar uma barra de progresso, pois este loop pode ser demorado.
    for initial_node in tqdm(G.nodes(), desc="Simulating outbreaks"):
        # Rodamos a simulação sem `return_full_data` para ser mais rápido.
        # A função retorna tuplas de arrays (t, S, I, R).
        t, S, I, R = EoN.fast_SIR(G, tau, gamma, initial_infecteds=[initial_node])
        
        # O tamanho final do incêndio é o último valor do array R.
        final_size = R[-1]
        fire_outbreak_sizes[initial_node] = final_size

    # --- 2. IDENTIFICAR E LOGAR OS TOP 5 ---
    # Ordena os nós pelo tamanho do incêndio que eles causaram (do maior para o menor).
    sorted_nodes = sorted(fire_outbreak_sizes.items(), key=lambda item: item[1], reverse=True)

    top_5_critical_nodes = sorted_nodes[:5]

    log.info("=" * 50)
    log.info("Top 5 Most Dangerous Ignition Points:")
    for i, (node_id, size) in enumerate(top_5_critical_nodes):
        log.info(f"{i+1}. Node {node_id}: Causes a fire of size {int(size)}")
    log.info("=" * 50)

    # --- 3. VISUALIZAR OS NÓS CRÍTICOS NO MAPA ---
    pos = {node: (data['Longitude'], data['Latitude']) for node, data in G.nodes(data=True)}
    
    # Definir cores e tamanhos para o plot
    node_colors = []
    node_sizes = []
    critical_node_ids = [node_id for node_id, size in top_5_critical_nodes]

    for node in G.nodes():
        if node in critical_node_ids:
            node_colors.append('red')   # Cor de destaque para nós críticos
            node_sizes.append(200)      # Tamanho maior para nós críticos
        else:
            node_colors.append('gray')  # Cor padrão para outros nós
            node_sizes.append(10)       # Tamanho padrão

    fig, ax = plt.subplots(figsize=(18, 12))

    # Desenha os nós de fundo
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes() if n not in critical_node_ids],
                           node_color='gray', node_size=10, alpha=0.5, ax=ax)
    # Desenha os nós críticos por cima
    nx.draw_networkx_nodes(G, pos, nodelist=critical_node_ids,
                           node_color='red', node_size=200, alpha=1.0, ax=ax,
                           label='Most Dangerous Ignition Points')

    plt.title("Top 5 Most Dangerous Ignition Points", fontsize=20)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    
    # Criar uma legenda
    plt.legend(scatterpoints=1, loc='upper right', fontsize=12)

    plt.savefig("../../data/critical_ignition_points.png", bbox_inches="tight")
    log.info("Map of critical ignition points saved to ../../data/critical_ignition_points.png")
