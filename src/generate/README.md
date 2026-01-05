# Graph Generation Module

This directory contains the scripts to build the network (graph) from the processed wildfire data.

## Functionality

The main script (`gen_graph.py`) reads the cleaned data and performs the following actions:

1.  Creates a node for each wildfire focus, storing its attributes (Latitude, Longitude, FRP, etc.).
2.  Adds edges between nodes based on a geographical proximity criterion (e.g., all focuses less than 50 km apart). The edge weight can represent the inverse distance.
3.  Saves the final `networkx` graph object in a `.gpickle` file in the `data/` directory. This file is the primary input for all analysis and visualization scripts.

The distance for creating edges is configurable via the `config.ini` file.
