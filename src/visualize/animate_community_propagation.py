import configparser
import itertools
import logging
import os
import pickle
import random

import EoN
import networkx as nx
from networkx.algorithms import community as nx_comm
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

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

    # --- 1. DETECÇÃO DE COMUNIDADES ---
    log.info("Detecting communities using Louvain algorithm...")
    communities = nx_comm.louvain_communities(G, weight='weight', seed=42)
    log.info(f"Found {len(communities)} communities.")

    # Criar um mapeamento de nó para ID da comunidade e cores
    node_to_community = {}
    for i, community in enumerate(communities):
        for node in community:
            node_to_community[node] = i
    
    color_cycle = itertools.cycle(plt.cm.get_cmap('tab20').colors)
    community_colors = [next(color_cycle) for _ in range(len(communities))]
    base_node_colors = [community_colors[node_to_community[node]] for node in G.nodes()]

    # --- 2. SIMULAÇÃO DE PROPAGAÇÃO ---
    gamma = 1.0
    tau = 0.8  # Usamos um valor de tau para o cenário de exemplo

    pos = {node: (data['Longitude'], data['Latitude']) for node, data in G.nodes(data=True)}
    # TODO: Idealmente seria interessante usar as datas do conjunto de dados para escolher os nós iniciais
    # e usar essas datas para ver como é a propagação de fato.
    initial_infected_node = random.choice(list(G.nodes()))
    log.info(f"Starting fire at node: {initial_infected_node} (Community ID: {node_to_community[initial_infected_node]})")

    log.info(f"Generating animation for tau = {tau}...")
    sim = EoN.fast_SIR(G, tau, gamma, initial_infecteds=[initial_infected_node], return_full_data=True)

    # --- 3. CONFIGURAÇÃO DA ANIMAÇÃO ---
    fig, ax = plt.subplots(figsize=(14, 9))

    times = sim.t()
    animation_times = [times[i] for i in range(0, len(times), len(times) // 150)] if len(times) > 150 else times

    def update(frame_time):
        ax.clear()

        statuses = sim.get_statuses(G.nodes(), frame_time)
        
        # Definir cores, tamanhos e opacidade com base no status
        node_colors = []
        node_sizes = []
        alphas = []
        
        for i, node in enumerate(G.nodes()):
            status = statuses[node]
            if status == 'S':
                node_colors.append(base_node_colors[i])
                node_sizes.append(20)
                alphas.append(0.4)
            elif status == 'I':
                node_colors.append(base_node_colors[i])
                node_sizes.append(150) # Nó queimando fica GRANDE
                alphas.append(1.0)
            else: # status == 'R'
                node_colors.append('black') # Nó queimado fica PRETO
                node_sizes.append(15)
                alphas.append(0.7)

        # Desenha a rede com as propriedades dinâmicas
        # O `alpha` não é um parâmetro direto do `draw`, então o aplicamos às cores
        rgba_colors = [(*plt.cm.colors.to_rgb(c), a) for c, a in zip(node_colors, alphas)]
        nx.draw(G, pos, ax=ax, with_labels=False, node_size=node_sizes, edgelist=[], node_color=rgba_colors)
        
        burning_edges = [(u, v) for u, v in G.edges() if statuses[u] == 'I' or statuses[v] == 'I']
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=burning_edges, edge_color='#ff9999', alpha=0.6)

        ax.set_title(f"Community Propagation (τ={tau}) at Time {frame_time:.2f}", fontsize=16)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # Legenda manual para os estados
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label='Burning', markerfacecolor='red', markersize=12),
                           plt.Line2D([0], [0], marker='o', color='w', label='Burned-out', markerfacecolor='black', markersize=8)]
        ax.legend(handles=legend_elements, loc='upper right', title="Status")

    anim = FuncAnimation(fig, update, frames=animation_times, interval=100, repeat_delay=1000)

    output_filename = f"../../data/community_propagation_animation_tau_{str(tau).replace('.', '_')}.gif"
    log.info(f"Saving animation to {output_filename}... (This may take a moment)")
    anim.save(output_filename, writer='pillow')
    plt.close(fig)

    log.info("Animation generated.")
