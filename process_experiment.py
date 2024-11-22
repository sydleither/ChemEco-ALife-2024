import os
import sys

import pandas as pd

from common import get_data_path


def main(exp_name):
    exp_dir = get_data_path(exp_name)
    exp_raw_dir = get_data_path(exp_name, "chem_eco")
    results = []
    for matrix_name in os.listdir(exp_raw_dir):
        df = pd.read_csv(f"{exp_raw_dir}/{matrix_name}/ranked_threshold_communities_scores.csv")
        graph_type, ew = matrix_name.split("_")
        score = df["logged_mult_score"][0]
        num_communities = len(df)
        result = {"graph_type":graph_type,
                  "edge_weights": ew,
                  "score":score, 
                  "num_communities":num_communities}
        results.append(result)
    df = pd.DataFrame(results)
    df.to_csv(f"{exp_dir}/results.csv", index=False)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Please provide an experiment name.")