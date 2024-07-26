import os

from constants import COMPRESSED_DIR

def download_lichess_data():
    os.makedirs(COMPRESSED_DIR, exist_ok=True)
    for year in range(2013, 2014):  # This will cover 2021, 2022, 2023, 2024
        for month in range(1, 3):
            url = f"https://database.lichess.org/standard/lichess_db_standard_rated_{year}-{month:02d}.pgn.zst"
            print(f"Downloading: {url}")
            os.system(f"wget -P {COMPRESSED_DIR} {url}")

if __name__ == "__main__":
    download_lichess_data()