#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to check if a command was successful
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

echo "Starting chess data processing pipeline"

# 0. Install required packages
echo "Step 0: Installing required packages"
if ! command -v pip &> /dev/null; then
    echo "pip could not be found. Please install pip and try again."
    exit 1
fi
pip install -r requirements.txt
check_status "Package installation"

# 1. Download
echo "Step 1: Downloading data"
python download_lichess.py
check_status "Download"

# 2. Uncompress
echo "Step 2: Uncompressing data"
python uncompress_zst.py --input_dir ./games/compressed
check_status "Uncompression"

# 3. Split into chunks
echo "Step 3: Splitting data into chunks"
python split_in_chunks.py  --input_dir ./games
check_status "Splitting"

# 4. Bin by Elo
echo "Step 4: Binning data by Elo"
python elo_bin.py --input_dir ./games/splits
check_status "Elo binning"

# 5. Compress
echo "Step 5: Compressing binned data"
python zstd_compress_elo_bin.py
check_status "Compression"

echo "Chess data processing pipeline completed successfully"