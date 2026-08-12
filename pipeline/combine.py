import pandas as pd


def combine_sources(source_a, source_b, source_c):
    columns = [
        "SRC",
        "ZIP3",
        "BIRTH_YEAR",
        "SERVICE_DATE",
        "DIAGNOSIS_CODE",
        "DIAGNOSIS_DESC",
        "PLACE_OF_SERVICE",
        "RENDERING_NPI",
        "REFERRING_NPI",
        "BILLING_NPI",
        "PATIENT_ID",
        "CLAIM_ID",
        "PRIMARY_PLAN_ID",
        "BILLED_AMOUNT",
        "GENDER"
    ]

    source_a = source_a[columns].copy()
    source_b = source_b[columns].copy()
    source_c = source_c[columns].copy()

    combined = pd.concat(
        [source_a, source_b, source_c],
        ignore_index=True
    )

    return combined


def remove_duplicates(df):
    key_columns = [
        "SRC",
        "CLAIM_ID",
        "DIAGNOSIS_CODE"
    ]

    before = len(df)

    df = df.drop_duplicates(
        subset=key_columns,
        keep="first"
    ).copy()

    dropped = before - len(df)

    return df, dropped


def prepare_final_output(df):
    columns = [
        "SRC",
        "ZIP3",
        "BIRTH_YEAR",
        "SERVICE_DATE",
        "DIAGNOSIS_CODE",
        "DIAGNOSIS_DESC",
        "PLACE_OF_SERVICE",
        "RENDERING_NPI",
        "REFERRING_NPI",
        "BILLING_NPI",
        "PATIENT_ID",
        "CLAIM_ID",
        "PRIMARY_PLAN_ID",
        "BILLED_AMOUNT",
        "GENDER"
    ]

    return df[columns].copy()