import pandas as pd
import requests

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

if __name__ == "__main__":
    url='https://drive.google.com/file/d/1l7W0B2MlYWQFH981haUA9h_6w8Q4sfpS/view?usp=sharing'
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]

    csv_file='../../data/queimadas.csv'
    download_csv(url, output_path=csv_file)

    df = pd.read_csv(csv_file)
    print(df.describe())


