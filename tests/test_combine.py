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
from pipeline.diagnosis import (
    process_source_a_diagnosis,
    process_source_b_diagnosis,
    process_source_c_diagnosis
)
from pipeline.enrichment import enrich_diagnosis
from pipeline.combine import (
    combine_sources,
    remove_duplicates
)


def prepare_source_a():
    source_a, _, _, dictionary = load_data()

    df = standardize_source_a(source_a)
    df = clean_source_a(df)
    df, _ = filter_valid_records(df)
    df = process_source_a_diagnosis(df)
    df = enrich_diagnosis(df, dictionary)

    return df


def prepare_source_b():
    _, source_b, _, dictionary = load_data()

    df = standardize_source_b(source_b)
    df = clean_source_b(df)
    df, _ = filter_valid_records(df)
    df = process_source_b_diagnosis(df)
    df = enrich_diagnosis(df, dictionary)

    return df


def prepare_source_c():
    _, _, source_c, dictionary = load_data()

    df = standardize_source_c(source_c)
    df, _ = clean_source_c(df)
    df, _ = filter_valid_records(df)

    df = process_source_c_diagnosis(df)
    df = enrich_diagnosis(df, dictionary)

    return df


def test_combine_sources():

    source_a = prepare_source_a()
    source_b = prepare_source_b()
    source_c = prepare_source_c()

    combined = combine_sources(
        source_a,
        source_b,
        source_c
    )

    assert len(combined) > 0
    assert set(combined["SRC"].unique()) == {
        "SRC_A",
        "SRC_B",
        "SRC_C"
    }


def test_final_grain():

    source_a = prepare_source_a()
    source_b = prepare_source_b()
    source_c = prepare_source_c()

    combined = combine_sources(
        source_a,
        source_b,
        source_c
    )

    combined, _ = remove_duplicates(combined)

    duplicates = combined.duplicated(
        subset=[
            "SRC",
            "CLAIM_ID",
            "DIAGNOSIS_CODE"
        ]
    )

    assert duplicates.sum() == 0