from itertools import product
import json
import os
import sys

from common import abbreviate_property_name, get_code_location, get_configs_path, get_properties_of_interest


def get_range_of_values(constraint):
    if constraint == "diameter":
        return [2, 3, 4, 5, 6]
    elif constraint == "in_degree_distribution" or constraint == "out_degree_distribution":
        return ["basically_exp", "basically_norm"]
    elif constraint.startswith("number"):
        return [0, 10, 20, 30]
    elif constraint == "average_negative_interactions_strength":
        return [-0.2, -0.4, -0.6, -0.8]
    else:
        return [0.2, 0.4, 0.6, 0.8]


def experiment_config(save_dir, exp_dir, exp_name, eval_funcs, network_size=10, num_generations=500, popsize=500):
    config = {
        "data_dir": exp_dir,
        "name": exp_name,
        "reps": 1,
        "save_data": 1,
        "plot_data": 0,
        "scheme": "NSGAII",
        "mutation_rate": 0.005,
        "mutation_odds": [1,2,1],
        "crossover_odds": [1,2,2],
        "crossover_rate": 0.6,
        "weight_range": [-1,1],
        "popsize": popsize,
        "network_size": network_size,
        "num_generations": num_generations,
        "eval_funcs": eval_funcs
    }

    config_path = f"{save_dir}{exp_dir}/{exp_name}.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


def multiple_constraint_experiment(exp_dir, constraint_combo):
    configs_path = get_configs_path()
    if not os.path.exists(configs_path+exp_dir):
        os.makedirs(configs_path+exp_dir)

    target_indicators = ["name" if c.endswith("distribution") else "target" for c in constraint_combo]
    target_values = [get_range_of_values(c) for c in constraint_combo]
    target_funcs = list(product(*target_values))

    eval_funcs = []
    for targets in target_funcs:
        eval_func = {constraint_combo[i]:{target_indicators[i]:targets[i]} for i in range(len(constraint_combo))}
        eval_func["weak_components"] = {"target":1}
        eval_funcs.append(eval_func)

    config_names = []
    for i,eval_func in enumerate(eval_funcs):
        exp_name = i
        experiment_config(configs_path, exp_dir, exp_name, eval_func, network_size=10, num_generations=500, popsize=500)
        config_names.append(exp_name)
    
    return config_names


def single_constraint_experiment(exp_dir, constraint):
    configs_path = get_configs_path()
    if not os.path.exists(configs_path+exp_dir):
        os.makedirs(configs_path+exp_dir)

    eval_funcs = []
    if constraint.endswith("distribution"):
        target_indicator = "name"
    else:
        target_indicator = "target"
    for x in get_range_of_values(constraint):
        eval_funcs.append(
            {
            "weak_components": {"target": 1},
            constraint: {target_indicator: x}
            }
        )

    config_names = []
    for i,eval_func in enumerate(eval_funcs):
        exp_name = i
        experiment_config(configs_path, exp_dir, exp_name, eval_func, network_size=10, num_generations=500, popsize=500)
        config_names.append(exp_name)
    
    return config_names


def cpip_experiment(exp_dir):
    configs_path = get_configs_path()
    if not os.path.exists(configs_path+exp_dir):
        os.makedirs(configs_path+exp_dir)

    eval_funcs = []
    for connectance in [0.2, 0.4, 0.6, 0.8]:
        for pip in [0.2, 0.4, 0.6, 0.8]:
            eval_funcs.append(
                {
                "weak_components": {"target": 1},
                "connectance": {"target": connectance},
                "positive_interactions_proportion": {"target": pip}
                }
            )

    config_names = []
    for i,eval_func in enumerate(eval_funcs):
        exp_name = i
        experiment_config(configs_path, exp_dir, exp_name, eval_func, network_size=10, num_generations=500, popsize=50)
        config_names.append(exp_name)
    
    return config_names


def capis_experiment(exp_dir):
    configs_path = get_configs_path()
    if not os.path.exists(configs_path+exp_dir):
        os.makedirs(configs_path+exp_dir)

    eval_funcs = []
    for connectance in [0.2, 0.4, 0.6, 0.8]:
        for apis in [0.2, 0.4, 0.6, 0.8]:
            eval_funcs.append(
                {
                "weak_components": {"target": 1},
                "connectance": {"target": connectance},
                "average_positive_interactions_strength": {"target": apis}
                }
            )

    config_names = []
    for i,eval_func in enumerate(eval_funcs):
        exp_name = i
        experiment_config(configs_path, exp_dir, exp_name, eval_func, network_size=10, num_generations=500, popsize=50)
        config_names.append(exp_name)
    
    return config_names


def topology_experiment(exp_dir):
    configs_path = get_configs_path()
    if not os.path.exists(configs_path+exp_dir):
        os.makedirs(configs_path+exp_dir)

    eval_funcs = []
    for connectance in [0.2, 0.4, 0.6, 0.8]:
        eval_funcs.append(
            {
            "weak_components": {"target": 1},
            "connectance": {"target": connectance}
            }
        )

    config_names = []
    for i,eval_func in enumerate(eval_funcs):
        exp_name = i
        experiment_config(configs_path, exp_dir, exp_name, eval_func)
        config_names.append(exp_name)
    
    return config_names


def uniform_experiment(exp_dir):
    configs_path = get_configs_path()
    if not os.path.exists(configs_path+exp_dir):
        os.makedirs(configs_path+exp_dir)

    eval_func = {"weak_components": {"target": 1}}

    exp_name = 0
    experiment_config(configs_path, exp_dir, exp_name, eval_func, num_generations=0, popsize=500)
    config_names = [exp_name]
    
    return config_names


def test_experiment(exp_dir):
    configs_path = get_configs_path()
    if not os.path.exists(configs_path+exp_dir):
        os.makedirs(configs_path+exp_dir)

    eval_func = {"connectance":{"target":0.2}}

    exp_name = 0
    experiment_config(configs_path, exp_dir, exp_name, eval_func, network_size=10, num_generations=500, popsize=50)
    config_names = [exp_name]
    
    return config_names


def generate_scripts(exp_dir, config_names):
    code_location = get_code_location()
    configs_path = get_configs_path()

    with open(f"{configs_path}{exp_dir}/submit_experiments", "w") as f:
        for config_name in config_names:
            f.write(f"sbatch {code_location}score_config.sb {exp_dir} {config_name}\n")


def generate_scripts_batch(overall_exp_name, exp_dirs, config_names):
    code_location = get_code_location()
    configs_path = get_configs_path()

    output = []
    for i in range(len(exp_dirs)):
        for config_name in config_names[i]:
            output.append(f"sbatch {code_location}score_config.sb {exp_dirs[i]} {config_name}\n")

    chunks = []
    for i in range(0, len(output), 150):
        chunks.append(output[i:i + 150])

    for i in range(len(chunks)):
        with open(f"{configs_path}/submit_{overall_exp_name}_experiments{i}", "w") as f:
            for output_line in chunks[i]:
                f.write(output_line)

    with open(f"{configs_path}/run_{overall_exp_name}_analysis", "w") as f:
        for j in range(len(exp_dirs)):
            f.write(f"python3 save_properties.py {exp_dirs[j]}\n")
        for j in range(len(exp_dirs)):
            f.write(f"python3 analysis.py {exp_dirs[j]}\n")


if __name__ == "__main__":
    experiment_name = sys.argv[1]
    if experiment_name == "single":
        all_config_names = []
        all_exp_names = []
        for constraint in get_properties_of_interest():
            exp_name = abbreviate_property_name(constraint, 1)
            all_exp_names.append(exp_name)
            all_config_names.append(single_constraint_experiment(exp_name, constraint))
        generate_scripts_batch(experiment_name, all_exp_names, all_config_names)
        exit()
    elif experiment_name == "double":
        constraint_combos = [
            ("connectance", "average_positive_interactions_strength"),
            ("connectance", "average_negative_interactions_strength"),
            ("connectance", "positive_interactions_proportion"),
            ("connectance", "diameter"),
            ("in_degree_distribution", "average_positive_interactions_strength"),
            ("in_degree_distribution", "average_negative_interactions_strength"),
            ("in_degree_distribution", "positive_interactions_proportion"),
            ("in_degree_distribution", "diameter"),
            ("diameter", "average_positive_interactions_strength"),
            ("diameter", "average_negative_interactions_strength"),
            ("diameter", "positive_interactions_proportion"),
            ("in_degree_distribution", "out_degree_distribution"),
            ("number_of_mutualistic_pairs", "number_of_competiton_pairs"),
            ("number_of_mutualistic_pairs", "number_of_parasitism_pairs"),
            ("number_of_competiton_pairs", "number_of_parasitism_pairs")
        ]
        all_config_names = []
        all_exp_names = []
        for constraints in constraint_combos:
            exp_name = "".join([abbreviate_property_name(c_i, 1) for c_i in constraints])
            all_exp_names.append(exp_name)
            all_config_names.append(multiple_constraint_experiment(exp_name, constraints))
        generate_scripts_batch(experiment_name, all_exp_names, all_config_names)
        exit()
    elif experiment_name == "test":
        config_names = test_experiment(experiment_name)
    elif experiment_name == "uniform":
        config_names = uniform_experiment(experiment_name)
    elif experiment_name == "topology":
        config_names = topology_experiment(experiment_name)
    elif experiment_name == "capis":
        config_names = capis_experiment(experiment_name)
    elif experiment_name == "cpip":
        config_names = cpip_experiment(experiment_name)
    else:
        print("Invalid experiment name.")
        exit()
    generate_scripts(experiment_name, config_names)