import pandas as pd
import requests
from requests import HTTPError
import basedosdados as bd


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

    print(f"CSV downloaded and saved to {output_path}")


def download_big_query(output_path):
    """
    Lib documentation https://basedosdados.org/docs/api_reference_python
    billing_id Project that will be billed. Find your Project ID here https://console.cloud.google.com/projectselector2/home/dashboard.
    :param output_path:
    """
    # REPLACE WITH YOUR PROJECT ID
    print("Enter your Project ID from google cloud console,\n"
          "for reference check  https://basedosdados.org/docs/api_reference_python .\n"
          "eg. mo412-queimadas-em-sp")
    billing_id = input()

    query = """
        SELECT
          `dias_sem_chuva`,
          `latitude`,
          `longitude`,
          `potencia_radiativa_fogo`,
          `precipitacao`,
          `risco_fogo`,
        FROM
          `basedosdados.br_inpe_queimadas.microdados`
        WHERE
          (`ano` IN (2024))
          AND (`mes` IN (9))
          AND (`sigla_uf` IN ('SP'))
          AND (`satelite` IN ('TERRA_M-M','TERRA_M-T'));
            """

    df = bd.read_sql(query=query, billing_project_id=billing_id)
    df.rename(columns={'longitude': 'Longitude', 'latitude': 'Latitude', 'potencia_radiativa_fogo': 'FRP'}, inplace=True)
    df.drop(columns=['sigla_uf', 'ano', 'mes', 'satelite'], inplace=True)
    df.to_csv(output_path, index=False, header=True)
    return df


if __name__ == "__main__":
    url='https://drive.google.com/file/d/1l7W0B2MlYWQFH981haUA9h_6w8Q4sfpS/view?usp=sharing'
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]

    csv_file='../../data/queimadas.csv'
    try:
        download_csv(url, output_path=csv_file)
        df = pd.read_csv(csv_file)
    except HTTPError as e:
        print(f"Error downloading CSV: {e}")
        df = download_big_query(output_path=csv_file)

    print(df.describe())


