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