# MO412 - Queimadas em SP

This project analyzes wildfire data in São Paulo (SP) using complex networks. It includes scripts for downloading data, generating graphs based on geographic proximity, and visualizing the results.

Portuguese version available [here](src/README_pt.md).

## Usage with Makefile

The project uses a hierarchical `Makefile` structure to manage the workflow.

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Running the Pipeline

To run the entire pipeline (install dependencies, download data, generate graphs, and create visualizations), simply run the following command from the root directory:

```bash
make
```

This will:
1. Install required Python packages from `src/requirements.txt`.
2. Create a `data/` directory at the project root for outputs.
3. Download wildfire data based on the configuration.
4. Generate networks (graphs) from the data.
5. Produce visualizations and analysis reports.

### Cleaning Up

To remove all generated data and temporary files:

```bash
make clean
```

### Sub-modules

You can also run specific parts of the pipeline by navigating to the `src/` directory and using `make` with subdirectories:
- `make data`: Only download data.
- `make generate`: Only generate graphs (requires data).
- `make visualize`: Only produce plots (requires graphs).

## Configuration (config.ini)

The behavior of the scripts is controlled by the `src/config.ini` file.

### [DEFAULT]
- `log_level`: Sets the verbosity of the logs (e.g., `INFO`, `DEBUG`, `WARNING`).

### [data]
- `query`: Whether to query BigQuery for new data using the `basedosdados` library. If false, it will fetch an example csv from Google Drive, which is not maintained by the author.
- `year`: The year of interest (e.g., `2024`).
- `month`: Comma-separated list of months (e.g., `8,9,10`).
- `state`: The Brazilian state abbreviation (e.g., `SP`).
- `satellites`: Specific satellites to filter data from.

### [generate]
- `merge_distance`: Distance in km to merge multiple fire spots into a single node.
- `add_edges_distance`: Distance threshold (km) for creating edges in the first graph (`graph_1_10.gpickle`).
- `add_edges_distance2`: Distance threshold (km) for creating edges in the second graph (`graph_50.gpickle`).

## Making Queries (BigQuery)

The project can download data directly from Google BigQuery using the `basedosdados` Python library.

### Prerequisites for Querying

1.  **Google Cloud Project**: You must have a project on Google Cloud Console.
2.  **Project ID**: You will need your [Project ID](https://console.cloud.google.com/projectselector2/home/dashboard) for billing purposes (BigQuery has a free tier).
3.  **Authentication**: When running the query for the first time, the `basedosdados` library will prompt you to authenticate in your browser.

### How it Works

When `query = true` is set in the `[data]` section of `config.ini`:

1.  The script `src/data/download_data.py` will prompt you to enter your **Google Cloud Project ID**.
2.  It constructs a SQL query targeting the `basedosdados.br_inpe_queimadas.microdados` table.
3.  The query filters the data based on the `year`, `month`, `state`, and `satellites` parameters defined in `config.ini`.
4.  The results are downloaded and saved to `data/queimadas.csv`.

For more detailed information on the underlying library, refer to the [basedosdados Python API documentation](https://basedosdados.org/docs/api_reference_python).

## Manual Execution

If you wish to run Python scripts manually, you must set the `CONFIG` environment variable to point to your configuration file:

```bash
export CONFIG="src/config.ini"
python src/data/download_data.py
```
