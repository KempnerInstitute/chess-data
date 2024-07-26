import os
import argparse

from constants import SPLITS_DIR

def main(input_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(SPLITS_DIR, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith('pgn'):
            source_dir = os.path.join(input_dir, file)
            dest_dir = os.path.join(SPLITS_DIR, file)
            os.system(f"split -d -n l/32 {source_dir} {dest_dir}.")
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Splits .pgn files in 32 chunks.')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing .pgn files')
    args = parser.parse_args()
    main(args.input_dir)
