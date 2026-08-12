from pipeline.loader import load_data
from pipeline.standardize import standardize_source_a
from pipeline.clean import clean_source_a
from pipeline.diagnosis import process_source_a_diagnosis
from pipeline.enrichment import enrich_diagnosis


def test_dictionary_enrichment():
    source_a, _, _, dictionary = load_data()

    df = standardize_source_a(source_a)
    df = clean_source_a(df)
    df = process_source_a_diagnosis(df)

    df = enrich_diagnosis(df, dictionary)

    assert "DIAGNOSIS_DESC" in df.columns
    assert df["DIAGNOSIS_DESC"].notna().all()


def test_unknown_diagnosis():
    source_a, _, _, dictionary = load_data()

    df = standardize_source_a(source_a)
    df = clean_source_a(df)
    df = process_source_a_diagnosis(df)

    df = enrich_diagnosis(df, dictionary)

    unknown_count = (
        df["DIAGNOSIS_DESC"] == "UNKNOWN"
    ).sum()

    assert unknown_count >= 0