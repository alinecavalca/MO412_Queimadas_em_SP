# Wildfire Focus Analysis in SP with Graph Theory

This directory contains the source code for the project analyzing the network of wildfire focuses in the state of São Paulo. The goal is to use graph theory to model the relationship between fire focuses, identify critical points, and simulate fire propagation.

## Directory Structure

The code is organized into the following subdirectories, which represent the stages of the analysis pipeline:

- **/data**: Scripts to download, clean, and format the raw wildfire focus data.
- **/generate**: Scripts to build the graph from the processed data, saving the graph object in `.gpickle` format.
- **/visualize**: Scripts to perform analysis on the generated graph, producing visualizations (graphs, maps, animations) and reports.

## Execution with Makefile (Automated Mode)

This project includes a main Makefile in `src/` that automates the entire pipeline: dependency installation, data processing, graph generation, and analysis.
The Makefile also automatically calls the Makefiles in the subdirectories.

### 🔧 make all

To execute the entire pipeline with a single command:

```bash
make all
```

What this command does:

1. Installs dependencies via `pip install -r requirements.txt`.

2. Creates the `data/` directory where logs, results, and intermediate files will be stored.

3. Copies the `config.ini` file to `data/` to record which configuration the execution was performed with.

4. Automatically enters the `data`, `generate`, and `visualize` directories, executing the corresponding `make` for each.

5. During execution:

    * the `CONFIG` environment variable is exported to each subdirectory;

    * all output (stdout and stderr) is recorded in `data/log.txt`, in addition to appearing on the screen.

In other words, the command walks through the subdirectories and executes their content automatically, maintaining a complete log of the execution.

### 🧹 make clean

To clean all generated artifacts:

```bash
make clean
```

This command:

* calls `make clean` inside each subdirectory (`data`, `generate`, `visualize`);

* completely removes the `data/` directory, deleting results, logs, and temporary files.


## Manual Execution (Without Makefile)

If the user prefers to execute each step manually, simply follow the logical order of the pipeline:

### Prerequisites

Before running the scripts, ensure you have Python 3 installed and the following libraries:

```bash
pip install -r requirements.txt
```

## Configuration

The project uses a configuration file to manage parameters such as file paths, log levels, and analysis parameters. Before executing, you must export the `CONFIG` environment variable pointing to your configuration file.

```bash
# Example of how to configure in the terminal
export CONFIG=/full/path/to/your/config.ini
```

## How to Run the Pipeline

The execution must follow the logical order of data processing.

1.  **Process Data:**
    Navigate to `src/data` and run the main script to get the cleaned data.
    ```bash
    cd src/data
    python download_data.py
    ```

2.  **Generate the Graph:**
    With the cleaned data, generate the `.gpickle` file that represents the network.
    ```bash
    cd ../generate
    python gen_graph.py
    ```

3.  **Perform Analysis and Visualizations:**
    With the graph ready, run the analyses. The `Makefile` in the `visualize` directory automates the execution of all analysis scripts.
    ```bash
    cd ../visualize
    make
    ```

All results will be saved in the `data/` directory.
