# chess-data

## [Main dataset (939GB)](https://huggingface.co/datasets/ezipe/lichess_elo_binned)

## [Debug dataset (600MB)](https://huggingface.co/datasets/ezipe/lichess_elo_binned_debug)

This repository holds the files needed to recreate the two datasets above. The debug dataset is just a smaller version of the main dataset for quickly testing new code on your local machine, whilst the main dataset is meant to be downloaded on the machine that will actually be used for training, whether that's a server, workstation, or compute cluster. The data is originally retrieved from lichess Jan. 2021 to Mar. 2024, and is then binned into different elos. Each folder `1000`, `1100`, etc. corresponds to all games between `900-1000` and `1000-1100`, respectively. The main dataset contains roughly 3.2B games. Since each game is around 400 characters or so, this very roughly corresponds to ~1.3T tokens. These numbers were done back of hand, and could certainly be made more precise.

The debug dataset can be created from the main one using the following code:

```
import os
import shutil

def copy_first_file(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        if not files:
            continue  # Skip if there are no files in the current directory
        #if '.git' in

        # Get the relative path of the current directory with respect to the source_dir
        relative_path = os.path.relpath(root, source_dir)

        # Construct the corresponding target directory
        target_subdir = os.path.join(target_dir, relative_path)

        # Ensure the target subdirectory exists
        os.makedirs(target_subdir, exist_ok=True)

        # Copy the first file in the current directory to the target directory
        first_file = files[0]
        source_file_path = os.path.join(root, first_file)
        target_file_path = os.path.join(target_subdir, first_file)

        if '.git' in source_file_path:
            continue

        shutil.copy2(source_file_path, target_file_path)
        print(f"Copied {source_file_path} to {target_file_path}")

# Example usage
source_directory = "lichess_elo_binned"
target_directory = "lichess_elo_binned_debug"
copy_first_file(source_directory, target_directory)
```

