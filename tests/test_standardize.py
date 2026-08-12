from pipeline.loader import load_data
from pipeline.standardize import (
    standardize_source_a,
    standardize_source_b,
    standardize_source_c
)


def test_source_a_columns():
    source_a, _, _, _ = load_data()

    df = standardize_source_a(source_a)

    assert "PATIENT_ID" in df.columns
    assert "CLAIM_ID" in df.columns
    assert "SERVICE_DATE" in df.columns
    assert "BILLED_AMOUNT" in df.columns
    assert "SRC" in df.columns


def test_source_b_columns():
    _, source_b, _, _ = load_data()

    df = standardize_source_b(source_b)

    assert "PATIENT_ID" in df.columns
    assert "CLAIM_ID" in df.columns
    assert "SERVICE_DATE" in df.columns
    assert "RENDERING_NPI" in df.columns
    assert "PRIMARY_PLAN_ID" in df.columns


def test_source_c_columns():
    _, _, source_c, _ = load_data()

    df = standardize_source_c(source_c)

    assert "PATIENT_ID" in df.columns
    assert "CLAIM_ID" in df.columns
    assert "SERVICE_DATE" in df.columns
    assert "RENDERING_NPI" in df.columns
    assert "BILLED_AMOUNT" in df.columns