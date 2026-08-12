import pandas as pd


def normalize_code(code):
    if pd.isna(code):
        return None

    code = str(code).strip().upper()
    code = code.replace(".", "")

    if not code:
        return None

    return code


def process_source_a_diagnosis(df):
    diagnosis_columns = [
        "diagnosis_code_1",
        "diagnosis_code_2",
        "diagnosis_code_3",
        "diagnosis_code_4",
        "diagnosis_code_5",
        "diagnosis_code_6",
        "diagnosis_code_7",
        "diagnosis_code_8"
    ]

    df = df.copy()

    df = df.melt(
        id_vars=[
            col for col in df.columns
            if col not in diagnosis_columns
        ],
        value_vars=diagnosis_columns,
        value_name="DIAGNOSIS_CODE"
    )

    df["DIAGNOSIS_CODE"] = df["DIAGNOSIS_CODE"].apply(
        normalize_code
    )

    df = df.dropna(
        subset=["DIAGNOSIS_CODE"]
    )

    return df.drop(
        columns=["variable"]
    )


def process_source_b_diagnosis(df):
    df = df.copy()

    df["DIAGNOSIS_CODE"] = df["dx_code"].apply(
        normalize_code
    )

    df = df.dropna(
        subset=["DIAGNOSIS_CODE"]
    )

    return df


def process_source_c_diagnosis(df):
    df = df.copy()

    df["diagnosis_codes"] = df["diagnosis_codes"].fillna("")

    df["DIAGNOSIS_CODE"] = df["diagnosis_codes"].str.split("|")

    df = df.explode(
        "DIAGNOSIS_CODE"
    )

    df["DIAGNOSIS_CODE"] = df["DIAGNOSIS_CODE"].apply(
        normalize_code
    )

    df = df.dropna(
        subset=["DIAGNOSIS_CODE"]
    )

    return df


def remove_duplicate_diagnoses(df):
    return df.drop_duplicates(
        subset=[
            "SRC",
            "CLAIM_ID",
            "DIAGNOSIS_CODE"
        ]
    ).copy()