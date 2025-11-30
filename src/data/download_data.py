import configparser
import logging
import os

import pandas as pd
import requests
from requests import HTTPError
import basedosdados as bd

config_file = os.environ['CONFIG']
config = configparser.ConfigParser()
config.read(config_file)
logging.basicConfig(level=config.get('DEFAULT', 'log_level'))
log = logging.getLogger(os.path.basename(__file__))


def download_csv(url, output_path):
    """
    Download CSV from a URL and save it directly to a file.

    Args:
        url: URL to download CSV from
        output_path: Path where to save the CSV file
    """

    # Download and save the file
    response = requests.get(url)
    response.raise_for_status()  # Raise error if download failed

    # Save to file
    with open(output_path, 'wb') as f:
        f.write(response.content)

    log.info(f"CSV downloaded and saved to {output_path}")


def download_big_query(output_path):
    """
    Lib documentation https://basedosdados.org/docs/api_reference_python
    billing_id Project that will be billed. Find your Project ID here https://console.cloud.google.com/projectselector2/home/dashboard.
    :param output_path:
    """
    # REPLACE WITH YOUR PROJECT ID
    log.info("Enter your Project ID from google cloud console,\n"
          "for reference check  https://basedosdados.org/docs/api_reference_python .\n"
          "eg. mo412-queimadas-em-sp")
    billing_id = input()

    years = config.get("data", "year", fallback='2024').split(",")
    months = config.get("data", "month", fallback='9').split(",")
    states = config.get("data", "state", fallback='SP').split(",")
    satellites = config.get("data", "satellites").split(",")
    query = f"""
        SELECT
          `dias_sem_chuva`,
          `latitude`,
          `longitude`,
          `potencia_radiativa_fogo`,
          `precipitacao`,
          `risco_fogo`,
          `sigla_uf`,
          `ano`,
          `mes`,
        FROM
          `basedosdados.br_inpe_queimadas.microdados`
        WHERE
          (`ano` IN ({",".join(years)}))
          AND (`mes` IN ({",".join(months)}))
          AND (`sigla_uf` IN ('{"','".join(states)}'))
          AND (`satelite` IN ('{"','".join(satellites)}'));
            """

    log.info(query)
    df = bd.read_sql(query=query, billing_project_id=billing_id)
    log.info(df.describe())
    df.rename(columns={'longitude': 'Longitude', 'latitude': 'Latitude', 'potencia_radiativa_fogo': 'FRP'}, inplace=True)
    df.to_csv(output_path, index=False, header=True)
    return df


if __name__ == "__main__":
    success = False
    csv_file='../../data/queimadas.csv'
    df = None
    if not config.getboolean("data", "query", fallback=False):
        url='https://drive.google.com/file/d/1l7W0B2MlYWQFH981haUA9h_6w8Q4sfpS/view?usp=sharing'
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]
        try:
            download_csv(url, output_path=csv_file)
            df = pd.read_csv(csv_file)
            if config.has_option("data", "month"):
                log.warning(f"Ignoring parameters at {config_file}")
            success = True
        except HTTPError as e:
            log.info(f"Error downloading CSV: {e}")

    if not success:
        df = download_big_query(output_path=csv_file)

    if df is not None:
        log.info(df.describe())


