import json
import os
import pickle
import sys

import pandas as pd

from common import abbreviate_property_name, get_code_location, get_configs_path, get_processed_data_path, get_properties_of_interest, get_raw_data_path
sys.path.insert(0, f"{get_code_location()}graph-evolution")
from organism import Organism
from eval_functions import Evaluation


def calculate_properties(df):
    eval_obj = Evaluation()
    property_names = get_properties_of_interest()
    
    for property_name in property_names:
        property_name_abbrv = abbreviate_property_name(property_name)
        if property_name.endswith("distribution"):
            df[property_name_abbrv] = "0"
            for config_file in os.listdir(f"{get_configs_path()}{exp_name}"):
                if config_file.endswith(".json"):
                    dist_config = json.load(open(f"{get_configs_path()}{exp_name}/{config_file}"))
                    dist_name = dist_config["eval_funcs"][property_name]["name"]
                    df.loc[df["config_num"] == config_file[0:-5], property_name_abbrv] = dist_name
        else:
            eval_func = getattr(eval_obj, property_name)
            df[property_name_abbrv] = df["graph"].apply(eval_func)

    return df


def read_raw_data(exp_name):
    all_results = []
    raw_data_dir = f"{get_raw_data_path()}{exp_name}"
    for config_dir in os.listdir(raw_data_dir):
        full_config_path = f"{raw_data_dir}/{config_dir}"
        for rep_dir in os.listdir(full_config_path):
            results_path = f"{full_config_path}/{rep_dir}/results.pkl"
            if os.path.exists(results_path):
                with open(results_path, "rb") as f:
                    results = pickle.load(f)
                    all_results += results
            else:
                print(f"Results not found in {results_path}.")
    df = pd.DataFrame.from_dict(all_results)
    return df


def main(exp_name):
    df = read_raw_data(exp_name)
    df = calculate_properties(df)
    df["matrix"] = df["graph"].apply(lambda x: x.adjacencyMatrix)
    df = df.drop("graph", axis=1)
    df.to_pickle(f"{get_processed_data_path()}{exp_name}.pkl")

    print(exp_name)
    print(df[["config", "replicate"]].groupby(["config"]).count())
    print()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        exp_name = sys.argv[1]
        main(exp_name)
    else:
        print("Please provide an experiment name.")