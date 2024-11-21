import json
import pickle
import subprocess
import sys

import pandas as pd
from scipy.stats import qmc

from common import get_data_path


def main(exp_name, matrix_name):
    exp_dir = get_data_path(exp_name)
    exp_matrices_dir = get_data_path(exp_name, "matrices")
    exp_raw_dir = get_data_path(exp_name, "chem_eco")
    params = json.load(open(f"{exp_dir}/params.json"))
    ntypes = int(params["num_nodes"])
    diffusion = 0.05
    seeding = 0.05
    clear = 0.0

    chem_eco = subprocess.Popen(
        [(f"./chemical-ecology/chemical-ecology "
        f"-DIFFUSION {diffusion} "
        f"-SEEDING_PROB {seeding} "
        f"-PROB_CLEAR {clear} "
        f"-INTERACTION_SOURCE {exp_matrices_dir}/{matrix_name} "
        f"-SEED 42 "
        f"-MAX_POP {10000} "
        f"-WORLD_WIDTH 10 "
        f"-WORLD_HEIGHT 10 "
        f"-UPDATES {10000} "
        f"-N_TYPES {ntypes} "
        f"-OUTPUT_DIR {exp_raw_dir}/{matrix_name}")],
        shell=True, 
        stdout=subprocess.DEVNULL)
    return_code = chem_eco.wait()
    if return_code != 0:
        print("Error in a-eco, return code:", return_code)
        sys.stdout.flush()
        return

    # df = pd.read_csv("output/ranked_threshold_communities_scores.csv")
    # score = df["logged_mult_score"][0]
    # num_communities = len(df)

    # result = {
    #     "experiment": exp_name,
    #     "config": config_name,
    #     "config_num": config_num,
    #     "replicate": rep,
    #     "ntypes": ntypes,
    #     "seeding": seeding,
    #     "diffusion": diffusion,
    #     "clear": clear,
    #     "graph": org,
    #     "num_communities": num_communities,
    #     "score": score
    # }
    # results.append(result)

    # with open("results.pkl", "wb") as f:
    #     pickle.dump(results, f)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        exp_name = sys.argv[1]
        matrix_name = sys.argv[2]
        main(exp_name, matrix_name)
    else:
        print("Please give the valid arguments: experiment name and interaction network name.")
        exit()