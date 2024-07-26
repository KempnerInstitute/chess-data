import os
import argparse
import sys
import zstandard as zstd

from constants import GAMES_DIR

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        except PermissionError:
            print(f"Error: Permission denied when trying to create {directory}")
            sys.exit(1)
    elif not os.access(directory, os.W_OK):
        print(f"Error: No write permission for {directory}")
        sys.exit(1)

def uncompress_files(input_dir):
    ensure_directory_exists(GAMES_DIR)
    
    for file in os.listdir(input_dir):
        if file.endswith('.zst'):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(GAMES_DIR, file[:-4])  # Remove .zst extension
            print(f"Uncompressing: {file}")
            try:
                with open(input_path, 'rb') as compressed_file:
                    decompressor = zstd.ZstdDecompressor()
                    with open(output_path, 'wb') as decompressed_file:
                        decompressor.copy_stream(compressed_file, decompressed_file)
                print(f"Successfully uncompressed {file}")
            except Exception as e:
                print(f"Error uncompressing {file}: {str(e)}")
                return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uncompress .zst files in the specified directory.')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing .zst files')
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: {args.input_dir} is not a valid directory.")
        exit(1)

    print(f"Files will be uncompressed to: {GAMES_DIR}")
    print("Starting decompression process. This may take several hours and require about 20TB of free space.")
    uncompress_files(args.input_dir)
    print("Decompression process finished.")