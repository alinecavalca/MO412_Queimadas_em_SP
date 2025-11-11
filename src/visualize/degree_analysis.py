import pickle
from matplotlib import pyplot as plt

if __name__ == "__main__":
    with open("../../data/graph_50.gpickle", 'rb') as f:
        G1 = pickle.load(f)
        # Calcular o grau de cada nó
        degrees = [d for _, d in G1.degree()]

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
        plt.grid(alpha=0.3)
        plt.savefig(f"../../data/degree_distribution.png", bbox_inches="tight")

        plt.figure(figsize=(8, 5))
        plt.hist(degrees, bins=range(max(degrees) + 1), color='skyblue', edgecolor='black', density=True)
        plt.xscale('log')
        plt.yscale('log')
        plt.title("Degree Distribution (log-log scale)")
        plt.xlabel("Degree (k)")
        plt.ylabel("P(k)")
        plt.grid(alpha=0.3)
        plt.savefig(f"../../data/degree_distribution_log_log.png", bbox_inches="tight")