import os
import shutil
import argparse

# For each directory in the source directory, copy the first file to the target directory
def copy_first_file(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        if not files:
            continue  # Skip if there are no files in the current directory        

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
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create debug dataset from the main one specified.')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory the main dataset is stored in')
    args = parser.parse_args()
    
    # Source directory is the main dataset directory
    source_directory = args.input_dir
    # source_directory = "./games/uncompressed_elo_binned_shards"

    # Remove trailing slash if it exists
    if(source_directory[-1] == '/'):
        source_directory = source_directory[:-1]

    # Target directory is the main dataset directory with "_debug" appended
    target_directory = source_directory + "_debug"

    copy_first_file(source_directory, target_directory)

