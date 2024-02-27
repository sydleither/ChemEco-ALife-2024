code_location = "/mnt/home/leithers/grant/ChemEco-ALife-2024/"


def get_code_location():
    return code_location


def get_configs_path():
    return code_location+"output/configs/"


def get_plots_path():
    return code_location+"output/plots/"


def get_processed_data_path():
    return code_location+"output/data/"


def get_raw_data_path():
    return "/mnt/scratch/leithers/chemical-ecology/alife2024/"


def get_non_property_column_names():
    return ["experiment", "config", "config_num", "replicate", "score", "ntypes", "matrix"]


def get_properties_of_interest():
    return ["connectance", "diameter", "clustering_coefficient", "transitivity", "number_of_modules", #topology
            "number_of_mutualistic_pairs", "number_of_competiton_pairs", "number_of_parasitism_pairs", #motif
            "average_positive_interactions_strength", "average_negative_interactions_strength", "positive_interactions_proportion" #weight
            ]


def abbreviate_property_name(property_name, n=3):
    split_name = property_name.split("_")

    if n == 1:
        abbrv_name = [x[0:n] for x in split_name]
        return "".join(abbrv_name)

    if len(split_name) == 1:
        abbrv_name = split_name
    else:
        abbrv_name = [x[0:n] for x in split_name]
    return "_".join(abbrv_name)