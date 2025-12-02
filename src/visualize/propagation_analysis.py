import configparser
import logging
import os
import pickle
import random

import EoN
import networkx as nx
from matplotlib import pyplot as plt

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

    log.info("Starting SIR propagation simulation...")

    # --- Parâmetros da Simulação ---
    # Estes valores são exemplos. O ideal seria calibrá-los com dados reais.

    # Taxa de recuperação (fogo se extingue).
    # Um valor de 1 significa que, em média, um incêndio em um local dura 1/1 = 1 unidade de tempo.
    gamma = 1.0

    # Escolher um nó aleatório para começar o incêndio
    # Usamos o mesmo nó inicial para todas as simulações para uma comparação justa
    # TODO: Idealmente seria interessante usar as datas do conjunto de dados para escolher os nós iniciais
    # e usar essas datas para ver como é a propagação de fato.
    initial_infected_node = random.choice(list(G.nodes()))

    log.info(f"Graph has {G.number_of_nodes()} nodes.")
    log.info(f"Starting fire at node: {initial_infected_node}")

    # Valores de tau para testar (baixo, médio, alto)
    tau_values = [0.1, 0.5, 1.0]

    # --- Plotar os Resultados usando Subplots ---
    # Criamos uma figura com 1 linha e 3 colunas de subplots.
    # `sharey=True` pode ajudar a comparar as alturas, mas vamos deixar como False
    # para que cada gráfico tenha sua própria escala e fique mais claro.
    fig, axes = plt.subplots(1, len(tau_values), figsize=(18, 5), sharex=True)
    fig.suptitle("SIR Propagation Analysis for Different Spread Rates (τ)", fontsize=16)
    
    # Iteramos sobre os eixos (subplots) e os valores de tau ao mesmo tempo
    for ax, tau in zip(axes, tau_values):
        log.info(f"Running simulation for tau = {tau}...")
        # Rodar a simulação SIR para o valor de tau atual
        sim = EoN.fast_SIR(G, tau, gamma, initial_infecteds=[initial_infected_node], return_full_data=True)
        
        # Plotar TODAS as três curvas (S, I, R) no subplot atual (ax)
        ax.plot(sim.t(), sim.S(), label='Susceptible')
        ax.plot(sim.t(), sim.I(), label='Burning')
        ax.plot(sim.t(), sim.R(), label='Burned-out')
        
        log.info(f"  -> Simulation finished. Total nodes burned: {sim.R()[-1]}")

        ax.set_title(f"τ = {tau}")
        ax.grid(alpha=0.3)
        ax.set_xlabel("Time")

    # Adicionar rótulo do eixo Y apenas no primeiro subplot para não poluir
    axes[0].set_ylabel("Number of Nodes")
    
    # Adicionar uma única legenda para a figura inteira
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.98, 0.88))
    
    plt.tight_layout(rect=[0, 0, 1, 0.96]) # Ajusta o layout para caber o supertítulo
    plt.savefig("../../data/sir_sensitivity_analysis.png", bbox_inches="tight")

    log.info("Sensitivity analysis plot saved to ../../data/sir_sensitivity_analysis.png")