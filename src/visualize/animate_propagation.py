
import configparser
import logging
import os
import pickle
import random

import EoN
import networkx as nx
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

    # --- Parâmetros da Simulação ---
    gamma = 1.0
    tau_values = [1.0]

    # Posições dos nós para o plot geográfico
    pos = {node: (data['Longitude'], data['Latitude']) for node, data in G.nodes(data=True)}

    # Usamos o mesmo nó inicial para todas as simulações para uma comparação justa
    # TODO: Idealmente seria interessante usar as datas do conjunto de dados para escolher os nós iniciais
    # e usar essas datas para ver como é a propagação de fato.
    initial_infected_node = random.choice(list(G.nodes()))
    log.info(f"Starting fire at node: {initial_infected_node} for all animations.")

    # Dicionário de cores para os status
    color_dict = {'S': '#a0a0a0', 'I': '#ff0000', 'R': '#303030'} # Cinza, Vermelho, Preto

    # Loop para criar uma animação para cada valor de tau
    for tau in tau_values:
        log.info(f"Generating animation for tau = {tau}...")

        # Roda a simulação para obter o objeto com todos os dados
        sim = EoN.fast_SIR(G, tau, gamma, initial_infecteds=[initial_infected_node], return_full_data=True)

        # --- Configuração da Animação ---
        fig, ax = plt.subplots(figsize=(12, 8))

        # Define os tempos para os frames da animação (ex: 100 frames)
        times = sim.t()
        animation_times = [times[i] for i in range(0, len(times), len(times) // 100)] if len(times) > 100 else times

        # Função que atualiza cada frame da animação
        def update(frame_time):
            ax.clear()

            # Obtém o status de todos os nós no tempo do frame
            statuses = sim.get_statuses(G.nodes(), frame_time)
            node_colors = [color_dict[statuses[node]] for node in G.nodes()]

            # Desenha a rede com as cores atualizadas
            nx.draw(G, pos, ax=ax, with_labels=False, node_size=20, edgelist=[], node_color=node_colors)
            # Desenha apenas as arestas que conectam a um nó queimando
            burning_edges = [(u, v) for u, v in G.edges() if statuses[u] == 'I' or statuses[v] == 'I']
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=burning_edges, edge_color='#ff9999', alpha=0.7)

            ax.set_title(f"Fire Propagation (τ={tau}) at Time {frame_time:.2f}")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            
            # Adiciona uma legenda manual
            legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label='Susceptible', markerfacecolor=color_dict['S'], markersize=10),
                               plt.Line2D([0], [0], marker='o', color='w', label='Burning', markerfacecolor=color_dict['I'], markersize=10),
                               plt.Line2D([0], [0], marker='o', color='w', label='Burned-out', markerfacecolor=color_dict['R'], markersize=10)]
            ax.legend(handles=legend_elements, loc='upper right')

        # Cria o objeto de animação
        anim = FuncAnimation(fig, update, frames=animation_times, interval=100, repeat_delay=1000)

        # Salva a animação como um GIF
        output_filename = f"../../data/propagation_animation_tau_{str(tau).replace('.', '_')}.gif"
        log.info(f"Saving animation to {output_filename}... (This may take a moment)")
        anim.save(output_filename, writer='pillow')
        plt.close(fig) # Fecha a figura para liberar memória

    log.info("All animations generated.")
