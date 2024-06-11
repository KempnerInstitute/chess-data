import os

in_folder = 'uncompressed_elo_binned_shards/'
out_folder = 'compressed_elo_binned_shards/'

for elo in os.listdir(in_folder):
    for fname in os.listdir(in_folder + elo):
        if fname.endswith('.zst'): continue
        os.makedirs(out_folder + elo, exist_ok=True)
        cm = f"zstd -T0 {in_folder}{elo}/{fname} -o {out_folder}{elo}/{fname}.zst"
        print(cm)
        os.system(cm)
