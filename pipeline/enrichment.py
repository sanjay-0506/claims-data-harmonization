import pandas as pd


def enrich_diagnosis(df, dictionary):
    df = df.copy()
    dictionary = dictionary.copy()

    dictionary["dx_code"] = (
        dictionary["dx_code"]
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(".", "", regex=False)
    )

    dictionary = dictionary[
        ["dx_code", "dx_description"]
    ].drop_duplicates("dx_code")

    df = df.merge(
        dictionary,
        how="left",
        left_on="DIAGNOSIS_CODE",
        right_on="dx_code"
    )

    df["DIAGNOSIS_DESC"] = (
        df["dx_description"]
        .fillna("UNKNOWN")
    )

    df = df.drop(
        columns=["dx_code", "dx_description"]
    )

    return df