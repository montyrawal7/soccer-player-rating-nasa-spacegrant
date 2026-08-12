import os
import urllib.request

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "ea_fc26_players.csv")
DATA_URL = "https://huggingface.co/datasets/Kishohar/footballIQ/resolve/main/ea_fc26_players.csv"

def download_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        print(f"Downloading dataset from HuggingFace to {CSV_PATH}...")
        urllib.request.urlretrieve(DATA_URL, CSV_PATH)
        print("Download complete!")
    else:
        print(f"Dataset already exists at {CSV_PATH}.")

if __name__ == "__main__":
    download_dataset()

