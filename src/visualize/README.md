# Graph Analysis and Visualization Module

This directory contains the scripts to analyze the wildfire focus graph and generate visualizations. Each script focuses on a different type of analysis, providing insights into the network structure, its robustness, and fire propagation dynamics.

## Analysis Scripts

Below is the description of each script and what it produces. To run all of them at once, use the `make` command in this directory.

- **`plot_graph.py`**:
  - **What it does:** Generates a basic geographic visualization of the graph, plotting wildfire focuses (nodes) at their latitude and longitude coordinates.
  - **Result:** A network map saved in `data/`.

- **`degree_analysis.py`**:
  - **What it does:** Performs a complete structural analysis of the network, calculating and plotting metrics such as degree distribution, clustering coefficient, and betweenness centrality. It also executes a robustness analysis, simulating node removal and measuring the impact on network connectivity.
  - **Results:** Distribution plots, a robustness analysis plot, and logs with key metrics.

- **`community_analysis.py`**:
  - **What it does:** Applies the Louvain algorithm to detect "communities" or "clusters" of densely connected fire focuses.
  - **Result:** A network map where each community is colored differently, helping to identify "risk zones".

- **`propagation_analysis.py`**:
  - **What it does:** Uses the **SIR (Susceptible-Infected-Recovered)** epidemiological model to simulate fire propagation. Performs a sensitivity analysis for different propagation rates (`tau`).
  - **Result:** Graphs showing the evolution of the number of susceptible, burning, and burnt nodes over time for different scenarios.
  (This is an initial experiment; ideally, improvements should be made, using date data from the dataset and other information to achieve a more realistic result. It would also be interesting to cross-reference with other information to see the real impacts.)

- **`find_critical_nodes.py`**:
  - **What it does:** Performs the most critical analysis from a practical standpoint. It simulates a fire starting at *each node* of the network and measures the final size of the damage.
  - **Result:** Identifies and highlights on a map the **5 most dangerous ignition points** — those that, if a fire starts there, have the greatest potential to cause a large-scale disaster.

- **`animate_propagation.py`**:
  - **What it does:** Generates animations (GIFs) showing fire propagation on the geographic map for different `tau` scenarios.
  - **Result:** `.gif` files visualizing fire dynamics.
  (This is an initial experiment; ideally, improvements should be made, using date data from the dataset and other information to achieve a more realistic result. It would also be interesting to cross-reference with other information to see the real impacts.)

- **`animate_community_propagation.py`**:
  - **What it does:** Combines community detection with propagation simulation to create an advanced animation.
  - **Result:** A `.gif` animation showing fire spreading within and between different risk zones (communities).
  (This is an initial experiment; ideally, improvements should be made, using date data from the dataset and other information to achieve a more realistic result. It would also be interesting to cross-reference with other information to see the real impacts.)

## How to Run

Ensure the `graph_50.gpickle` file exists in the `data/` directory.

To run all analysis scripts in sequence:
```bash
make
```

To clean all generated files:
```bash
make clean
```
