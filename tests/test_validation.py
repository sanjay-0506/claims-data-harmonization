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
    process_source_c_diagnosis,
    remove_duplicate_diagnoses
)
from pipeline.enrichment import enrich_diagnosis
from pipeline.combine import (
    combine_sources,
    remove_duplicates,
    prepare_final_output
)
from pipeline.validation import validate_output


def build_output():
    source_a, source_b, source_c, dictionary = load_data()

    # Source A
    source_a = standardize_source_a(source_a)
    source_a = clean_source_a(source_a)
    source_a, _ = filter_valid_records(source_a)
    source_a = process_source_a_diagnosis(source_a)
    source_a = enrich_diagnosis(source_a, dictionary)
    source_a = remove_duplicate_diagnoses(source_a)

    # Source B
    source_b = standardize_source_b(source_b)
    source_b = clean_source_b(source_b)
    source_b, _ = filter_valid_records(source_b)
    source_b = process_source_b_diagnosis(source_b)
    source_b = enrich_diagnosis(source_b, dictionary)
    source_b = remove_duplicate_diagnoses(source_b)

    # Source C
    source_c = standardize_source_c(source_c)
    source_c, _ = clean_source_c(source_c)
    source_c, _ = filter_valid_records(source_c)
    source_c = process_source_c_diagnosis(source_c)
    source_c = enrich_diagnosis(source_c, dictionary)
    source_c = remove_duplicate_diagnoses(source_c)

    combined = combine_sources(
        source_a,
        source_b,
        source_c
    )

    combined, _ = remove_duplicates(combined)

    return prepare_final_output(combined)


def test_acceptance_checks():
    df = build_output()

    results = validate_output(df)

    for name, result in results.items():
        assert result["passed"], (
            f"{name} failed: {result}"
        )