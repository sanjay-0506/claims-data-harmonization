import pandas as pd
from pipeline.loader import load_data
from pipeline.standardize import (
    standardize_source_a,
    standardize_source_b,
    standardize_source_c
)
from pipeline.clean import (
    clean_source_a,
    clean_source_b,
    clean_source_c,
    filter_valid_records
)


def test_source_a_cleaning():
    source_a, _, _, _ = load_data()

    df = standardize_source_a(source_a)
    df = clean_source_a(df)

    assert df["SRC"].unique().tolist() == ["SRC_A"]
    assert pd.api.types.is_datetime64_any_dtype(df["SERVICE_DATE"])


def test_source_b_gender():
    _, source_b, _, _ = load_data()

    df = standardize_source_b(source_b)
    df = clean_source_b(df)

    assert set(df["GENDER"].dropna().unique()) == {"M", "F"}


def test_source_c_gender():
    _, _, source_c, _ = load_data()

    df = standardize_source_c(source_c)
    df, version_info = clean_source_c(df)

    assert set(df["GENDER"].dropna().unique()) == {"M", "F"}


def test_source_c_latest_version():
    _, _, source_c, _ = load_data()

    df = standardize_source_c(source_c)
    df, version_info = clean_source_c(df)

    assert len(df) == 20001
    assert version_info["dropped"] == 4185