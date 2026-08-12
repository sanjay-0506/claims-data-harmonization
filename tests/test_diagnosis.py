from pipeline.loader import load_data
from pipeline.standardize import (
    standardize_source_a,
    standardize_source_b,
    standardize_source_c
)
from pipeline.clean import (
    clean_source_a,
    clean_source_b,
    clean_source_c
)
from pipeline.diagnosis import (
    normalize_code,
    process_source_a_diagnosis,
    process_source_b_diagnosis,
    process_source_c_diagnosis,
    remove_duplicate_diagnoses
)


def test_normalize_code():
    assert normalize_code("E11.9") == "E119"
    assert normalize_code(" e11.9 ") == "E119"
    assert normalize_code("C50.911") == "C50911"


def test_source_a_diagnosis():
    source_a, _, _, _ = load_data()

    df = standardize_source_a(source_a)
    df = clean_source_a(df)
    df = process_source_a_diagnosis(df)

    assert "DIAGNOSIS_CODE" in df.columns
    assert df["DIAGNOSIS_CODE"].notna().all()


def test_source_b_diagnosis():
    _, source_b, _, _ = load_data()

    df = standardize_source_b(source_b)
    df = clean_source_b(df)
    df = process_source_b_diagnosis(df)

    assert "DIAGNOSIS_CODE" in df.columns
    assert df["DIAGNOSIS_CODE"].notna().all()


def test_source_c_diagnosis():
    _, _, source_c, _ = load_data()

    df = standardize_source_c(source_c)
    df, _ = clean_source_c(df)
    df = process_source_c_diagnosis(df)

    assert "DIAGNOSIS_CODE" in df.columns
    assert df["DIAGNOSIS_CODE"].notna().all()


def test_no_duplicate_grain():
    source_a, _, _, _ = load_data()

    df = standardize_source_a(source_a)
    df = clean_source_a(df)
    df = process_source_a_diagnosis(df)

    df = remove_duplicate_diagnoses(df)

    duplicates = df.duplicated(
        subset=[
            "SRC",
            "CLAIM_ID",
            "DIAGNOSIS_CODE"
        ]
    )

    assert duplicates.sum() == 0