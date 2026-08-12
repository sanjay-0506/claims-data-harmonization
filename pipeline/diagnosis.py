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

    rows = []

    for _, row in df.iterrows():
        for column in diagnosis_columns:
            code = normalize_code(row[column])

            if code is None:
                continue

            new_row = row.copy()
            new_row["DIAGNOSIS_CODE"] = code
            rows.append(new_row)

    return pd.DataFrame(rows)


def process_source_b_diagnosis(df):
    df = df.copy()

    df["DIAGNOSIS_CODE"] = df["dx_code"].apply(
        normalize_code
    )

    return df


def process_source_c_diagnosis(df):
    rows = []

    for _, row in df.iterrows():
        if pd.isna(row["diagnosis_codes"]):
            continue

        codes = str(row["diagnosis_codes"]).split("|")

        for code in codes:
            code = normalize_code(code)

            if code is None:
                continue

            new_row = row.copy()
            new_row["DIAGNOSIS_CODE"] = code
            rows.append(new_row)

    return pd.DataFrame(rows)


def remove_duplicate_diagnoses(df):
    return df.drop_duplicates(
        subset=[
            "SRC",
            "CLAIM_ID",
            "DIAGNOSIS_CODE"
        ]
    ).copy()