# chess-data

This repository holds the files needed to recreate the two datasets above. The debug dataset is just a smaller version of the main dataset for quickly testing new code on your local machine, whilst the main dataset is meant to be downloaded on the machine that will actually be used for training, whether that's a server, workstation, or compute cluster. The data is originally retrieved from [lichess](https://database.lichess.org/) Jan. 2021 to Mar. 2024, and is then binned into different elos. Each folder `1000`, `1100`, etc. corresponds to all games between `900-1000` and `1000-1100`, respectively. The main dataset contains roughly 3.2B games. Since each game is around 400 characters or so, this very roughly corresponds to ~1.3T tokens. These numbers were done back of hand, and could certainly be made more precise.

## Datasets

### [Main dataset (939GB)](https://huggingface.co/datasets/ezipe/lichess_elo_binned)

### [Debug dataset (600MB)](https://huggingface.co/datasets/ezipe/lichess_elo_binned_debug)

## Data Organization

Each folder (`1000`, `1100`, etc.) corresponds to games within specific Elo ranges:

- `1000`: 900-1000 Elo
- `1100`: 1000-1100 Elo
- And so on...

## System Requirements

- Storage: At least 20TB of free space for processing
- Processing time: Several hours for uncompression step

## Data Processing Pipeline

Note: verify the required packages in requirements.txt

The data processing pipeline goes in the following order:

1. Download
2. Uncompress
3. Split into chunks
4. Bin by Elo
5. Compress

To run the entire Data Processing Pipeline with default arguments, use the default.sh script.

### 1. Download

```bash
python download_lichess.py
```

### 2. Uncompress

Note: This step requires about 20TB of free space and may take several hours.

```bash
python uncompress_zst.py --input_dir /path/files/to/uncompress
```

### 3. Split into chunks

This step is necessary to allow the `zstd_process` in chess-research to open enough file handlers.

```bash
python split_in_chunks.py --input_dir /path/files/to/splits
```

### 4. Bin by Elo

```bash
python elo_bin.py  --input_dir /path/files/to/bin
```

### 5. Compress

```bash
python zstd_compress_elo_bin.py 
```

## Creating the Debug Dataset

The debug dataset can be created from the main one using the script `create_debug_dataset.py`, that picks the first file for each elo bin:

```bash
python create_debug_dataset.py --input_dir /path/to/the/dataset
```
