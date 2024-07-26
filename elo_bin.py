# data format example
# [Event "Rated Bullet game"]
# [Site "https://lichess.org/iML6DQBA"]
# [Date "2023.01.01"]
# [Round "-"]
# [White "dida0617"]
# [Black "Wizard_of_North"]
# [Result "1-0"]
# [UTCDate "2023.01.01"]
# [UTCTime "00:00:42"]
# [WhiteElo "1877"]
# [BlackElo "1936"]
# [WhiteRatingDiff "+7"]
# [BlackRatingDiff "-6"]
# [ECO "A00"]
# [Opening "Van Geet Opening"]
# [TimeControl "30+0"]
# [Termination "Time forfeit"]
# 1. Nc3 { [%clk 0:00:30] } 1... Nf6 { [%clk 0:00:30] } 2. Nf3 { [%clk 0:00:30] } 2... e6 { [%clk 0:00:30] } 3. d4 { [%clk 0:00:30] } 3... d5 { [%clk 0:00:29] } 4. e4 { [%clk 0:00:30] } 4... dxe4 { [%clk 0:00:28] } 5. Ng5 { [%clk 0:00:30] } 5... h6 { [%clk 0:00:27] } 6. Ngxe4 { [%clk 0:00:29] } 6... Nxe4 { [%clk 0:00:27] } 7. Nxe4 { [%clk 0:00:29] } 7... Be7 { [%clk 0:00:26] } 8. Qf3 { [%clk 0:00:28] } 8... Bf6 { [%clk 0:00:25] } 9. c3 { [%clk 0:00:26] } 9... O-O { [%clk 0:00:24] } 10. Bd3 { [%clk 0:00:25] } 10... c5 { [%clk 0:00:22] } 11. Nxf6+ { [%clk 0:00:24] } 11... Qxf6 { [%clk 0:00:21] } 12. Qxf6 { [%clk 0:00:23] } 12... gxf6 { [%clk 0:00:20] } 13. dxc5 { [%clk 0:00:23] } 13... b6 { [%clk 0:00:18] } 14. cxb6 { [%clk 0:00:22] } 14... axb6 { [%clk 0:00:18] } 15. Be3 { [%clk 0:00:21] } 15... Bb7 { [%clk 0:00:18] } 16. O-O { [%clk 0:00:19] } 16... Nc6 { [%clk 0:00:18] } 17. Bxb6 { [%clk 0:00:18] } 17... Ne5 { [%clk 0:00:17] } 18. Bc2 { [%clk 0:00:16] } 18... Rad8 { [%clk 0:00:16] } 19. Bb3 { [%clk 0:00:14] } 19... Rb8 { [%clk 0:00:15] } 20. Bc7 { [%clk 0:00:13] } 20... Rbc8 { [%clk 0:00:13] } 21. Bxe5 { [%clk 0:00:12] } 21... fxe5 { [%clk 0:00:12] } 22. Rae1 { [%clk 0:00:12] } 22... f6 { [%clk 0:00:12] } 23. f4 { [%clk 0:00:10] } 23... Kf7 { [%clk 0:00:11] } 24. fxe5 { [%clk 0:00:10] } 24... f5 { [%clk 0:00:10] } 25. g4 { [%clk 0:00:08] } 25... Kg6 { [%clk 0:00:08] } 26. gxf5+ { [%clk 0:00:08] } 26... exf5 { [%clk 0:00:08] } 27. Be6 { [%clk 0:00:06] } 27... Rg8 { [%clk 0:00:07] } 28. Bxc8 { [%clk 0:00:04] } 28... Kh5+ { [%clk 0:00:05] } 29. Kf2 { [%clk 0:00:04] } 29... Rg2+ { [%clk 0:00:04] } 30. Ke3 { [%clk 0:00:03] } 30... Rxh2 { [%clk 0:00:03] } 31. e6 { [%clk 0:00:03] } 31... Rh3+ { [%clk 0:00:02] } 32. Kd4 { [%clk 0:00:03] } 32... Bc6 { [%clk 0:00:02] } 33. Kc5 { [%clk 0:00:03] } 33... Be8 { [%clk 0:00:01] } 34. e7 { [%clk 0:00:02] } 34... Rh4 { [%clk 0:00:00] } 35. Be6 { [%clk 0:00:02] } 35... Rc4+ { [%clk 0:00:00] } 36. Kxc4 { [%clk 0:00:01] } 1-0
# in the future maybe i'll save a full dataset with all metadata. but for now let's just do elo binning without the game
# URL,whiteelo,blackelo,outcome,transcript
# iML6DQBA,1877,1936,1-0,1. e4 d4.....

import math
from typing import List, Optional

import io
import os
import random
import re
import time
import argparse

import numpy as np
import torch
import tqdm
import zstandard
from torch.utils.data import IterableDataset

from constants import BIN_SAVES_DIR

def process_wrapper():
    vocab = "#+-.0123456789;=BKNOQRabcdefghx "
    del_chars = "".join(c for c in map(chr, range(1114111)) if not c in vocab)
    del_map = str.maketrans("", "", del_chars)

    def process(game_str):
        res = {}

        for g in game_str.split("\n"):
            if g.startswith("["):
                k, v = g[1:-1].split(' "')
                res[k] = v[:-1]
            elif g.startswith("1. "):
                no_brackets_string = re.sub(r"\{.*?\}", "", g)  # , flags=re.DOTALL
                no_brackets_string = no_brackets_string.translate(del_map)
                remove_dots = re.sub(r"\b\d+\.\.\. ", "", no_brackets_string)
                remove_game_result = re.sub(r"1-0|0-1|1/2-1/2", "", remove_dots)[:-2]
                remove_spaces = re.sub(r"(\d+)\.\s+", r"\1.", remove_game_result)
                remove_double_spaces = re.sub(r"  ", r" ", remove_spaces)
                res["transcript"] = remove_double_spaces

        return res

    return process


def calculate_split(total_splits, total_len, index):
    assert (
        0 <= index < total_splits
    ), f"Index {index} out of bounds for {total_splits} splits."
    assert total_splits > 0, "Total splits must be greater than 0."
    assert total_len > 0, "Total length must be greater than 0."

    if total_len < total_splits:  # if there are more splits than work
        if index < total_len:
            return index, index + 1
        return 0, 0  # give no work

    # divide as fairly as possible
    if (total_len / total_splits) % 1 > 0.5:
        # Calculate the length of each split by ceiling
        split_length = -(total_len // -total_splits)
    else:
        # Calculate the length of each split by floor
        split_length = total_len // total_splits

    # Calculate the start and end indices of the split
    start_index = index * split_length
    end_index = start_index + split_length

    if start_index >= total_len:
        return 0, 0

    # Adjust the end index if the split is not evenly divided
    if index == total_splits - 1 or end_index > total_len:
        end_index = total_len

    return start_index, end_index


class StreamingPGNDataset(IterableDataset):  # TODO implement train test split
    def __init__(self, file_paths, seed=42, save_path=None):
        self.set_file_paths(file_paths, seed)
        self.process = process_wrapper()
        self.save_path = save_path
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def set_file_paths(self, file_paths, seed):
        self.file_paths = file_paths
        self.rng = random.Random(seed)
        self.rng.shuffle(self.file_paths)

    def read_game(self):
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is not None:  # multiprocessing
            # print('multiprocessing')
            assert worker_info.num_workers <= len(
                self.file_paths
            ), f"Num workers {worker_info.num_workers} greater than number of files {len(self.file_paths)}."
            start, end = calculate_split(
                worker_info.num_workers, len(self.file_paths), worker_info.id
            )
            self.file_paths = self.file_paths[start:end]
            # print(worker_info.id, start, end)
        # else:
        # print('not multiprocessing')

        def game_generator(path):
            with open(path, "r") as pgn_file:
                # stream_reader = dctx.stream_reader(pgn_file)
                # text_stream = io.TextIOWrapper(stream_reader, encoding="utf-8")

                fg = ""
                for i in pgn_file:
                    # yield i
                    fg += i
                    if i.startswith("1. "):
                        game = self.process(fg)
                        fg = ""
                        # print('\n\n', game)
                        yield game

        gen = [game_generator(file) for file in self.file_paths]
        fouts = {}

        i = 0
        # print(len(gen), gen)
        elo_bucket = "None"

        while len(gen) > 0:
            # print(i)
            # if i > 1000:
            #     return

            try:
                game = next(gen[i % len(gen)])
                if game.get("transcript") is None:
                    i += 1
                    continue

                if self.save_path is not None:

                    if (
                        game.get("WhiteElo") is not None
                        and game.get("BlackElo") is not None
                    ):
                        elo_bucket = str(
                            math.ceil(
                                max(
                                    int(game.get("WhiteElo")), int(game.get("BlackElo"))
                                )
                                / 100
                            )
                            * 100
                        )
                        # save into (elo_bucket - 100, elo_bucket)
                        # assert elo_bucket >= 100

                    try:
                        site = game.get("Site").split("/")[-1]
                    except:
                        site = None

                    file_path = self.file_paths[i % len(gen)].split("/")[-1]
                    save_str = f"{site},{game.get('WhiteElo')},{game.get('BlackElo')},{game.get('Result')},{game['transcript']}\n"
                    fout_key = f"{elo_bucket}_{file_path}"
                    if fouts.get(fout_key) is None:
                        os.makedirs(
                            os.path.join(self.save_path, elo_bucket), exist_ok=True
                        )
                        fouts[fout_key] = open(
                            os.path.join(self.save_path, elo_bucket, file_path), "w"
                        )

                    fouts[fout_key].write(save_str)

                if i % 10_000 == 0:
                    print('flushing!', torch.utils.data.get_worker_info().id)

                    [f.flush() for f in fouts.values()]
                    [os.fsync(f) for f in fouts.values()]
                # fouts[fout_key].flush() # slows things down by 20x
                # os.fsync(fouts[fout_key])

            except StopIteration:
                if self.save_path is not None:
                    file_path = self.file_paths[i % len(gen)].split("/")[-1]

                    del_keys = []
                    for fout in fouts:
                        if fout.endswith(file_path):
                            fouts[fout].close()
                            del_keys.append(fout)
                    for k in del_keys:
                        del fouts[k]

                del self.file_paths[i % len(gen)]
                del gen[i % len(gen)]
                continue

            i += 1
            yield game

            # parse txt

    def __iter__(self):
        return self.read_game()

# takes around 17 minutes to cycle through a single shard

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bin chess games by Elo rating.")
    parser.add_argument('--input_dir', type=str, required=True, help='Directory input files')

    args = parser.parse_args()

    input_dir = args.input_dir

    ############
    # StreamingPGNDataset
    ############

    # ds = StreamingPGNDataset(
    #     [
    #         os.path.join(input_dir, "lichess_db_standard_rated_2023-01.pgn.00")
    #     ],
    #     save_path=BIN_SAVES_DIR,
    # )
    # for k in tqdm.tqdm(ds):
    #     pass

    ############
    # StreamingBlockPGNDataset
    ############

    # Number of workers should be equal or less to the number of files in the input directory
    workers = 360

    ds_block = torch.utils.data.DataLoader(
        StreamingPGNDataset(
            [os.path.join(input_dir, k) for k in os.listdir(input_dir)],
            save_path=BIN_SAVES_DIR,
        ),
        num_workers=workers,
        batch_size=workers,
        collate_fn=lambda x: x
    )

    t = time.time()
    for _ in tqdm.tqdm(ds_block):
        pass
    end = time.time() - t

    print(f'Finished in {end} seconds!')