import pandas as pd


START_DATE = pd.Timestamp("2018-01-01")
END_DATE = pd.Timestamp("2025-02-28")


def clean_source_a(df):
    df = df.copy()

    df["SERVICE_DATE"] = pd.to_datetime(
        df["SERVICE_DATE"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    df["SRC"] = "SRC_A"

    return df


def clean_source_b(df):
    df = df.copy()

    df["SERVICE_DATE"] = pd.to_datetime(
        df["SERVICE_DATE"],
        errors="coerce"
    )

    df["GENDER"] = df["GENDER"].map({
        1: "M",
        2: "F"
    })

    df["SRC"] = "SRC_B"

    return df


def clean_source_c(df):
    df = df.copy()

    rows_in = len(df)

    df = (
        df.sort_values("version")
        .drop_duplicates("CLAIM_ID", keep="last")
    )

    rows_out = len(df)

    dropped = rows_in - rows_out

    df["SERVICE_DATE"] = pd.to_datetime(
        df["SERVICE_DATE"],
        errors="coerce"
    )

    df["GENDER"] = df["GENDER"].map({
        "Male": "M",
        "Female": "F"
    })

    df["SRC"] = "SRC_C"

    version_info = {
        "rows_in": rows_in,
        "rows_out": rows_out,
        "dropped": dropped,
        "reason": {
            "superseded_claim_version": dropped
        }
    }

    return df, version_info

def filter_valid_records(df):
    df = df.copy()

    before = len(df)

    missing_patient = df["PATIENT_ID"].isna() | (
        df["PATIENT_ID"].astype(str).str.strip() == ""
    )

    df = df[~missing_patient]

    after_patient = len(df)

    valid_date = df["SERVICE_DATE"].between(
        START_DATE,
        END_DATE
    )

    df = df[valid_date]

    after_date = len(df)

    dropped = {
        "missing_patient_id": before - after_patient,
        "outside_date_range": after_patient - after_date
    }

    return df, dropped