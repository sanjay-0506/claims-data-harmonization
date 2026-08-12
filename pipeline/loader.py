import pandas as pd


def load_data(data_dir="data"):
    source_a = pd.read_excel(
        f"{data_dir}/source_a_claims.csv.xlsx"
    )

    source_b = pd.read_excel(
        f"{data_dir}/source_b_claims.csv.xlsx"
    )

    source_c = pd.read_excel(
        f"{data_dir}/source_c_claims.csv.xlsx"
    )

    dictionary = pd.read_excel(
        f"{data_dir}/dx_dictionary.csv.xlsx"
    )

    return source_a, source_b, source_c, dictionary