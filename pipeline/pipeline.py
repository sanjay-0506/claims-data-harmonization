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

from pipeline.tracker import PipelineTracker


def run_pipeline(data_dir="data"):
    tracker = PipelineTracker()

    # Load data
    source_a, source_b, source_c, dictionary = load_data(
        data_dir
    )

    tracker.add_stage(
        "Load data",
        len(source_a) + len(source_b) + len(source_c),
        len(source_a) + len(source_b) + len(source_c)
    )

    # Source A
    source_a = standardize_source_a(source_a)
    source_a = clean_source_a(source_a)

    rows_in = len(source_a)

    source_a, dropped = filter_valid_records(
        source_a
    )

    tracker.add_stage(
        "Source A - validate records",
        rows_in,
        len(source_a),
        sum(dropped.values()),
        dropped
    )

    source_a = process_source_a_diagnosis(
        source_a
    )

    source_a = enrich_diagnosis(
        source_a,
        dictionary
    )

    source_a = remove_duplicate_diagnoses(
        source_a
    )

    # Source B
    source_b = standardize_source_b(source_b)
    source_b = clean_source_b(source_b)

    rows_in = len(source_b)

    source_b, dropped = filter_valid_records(
        source_b
    )

    tracker.add_stage(
        "Source B - validate records",
        rows_in,
        len(source_b),
        sum(dropped.values()),
        dropped
    )

    source_b = process_source_b_diagnosis(
        source_b
    )

    source_b = enrich_diagnosis(
        source_b,
        dictionary
    )

    source_b = remove_duplicate_diagnoses(
        source_b
    )

    # Source C
    source_c = standardize_source_c(source_c)

    source_c, version_info = clean_source_c(
        source_c
    )

    tracker.add_stage(
        "Source C - version resolution",
        version_info["rows_in"],
        version_info["rows_out"],
        version_info["dropped"],
        version_info["reason"]
    )

    rows_in = len(source_c)

    source_c, dropped = filter_valid_records(
        source_c
    )

    tracker.add_stage(
        "Source C - validate records",
        rows_in,
        len(source_c),
        sum(dropped.values()),
        dropped
    )

    source_c = process_source_c_diagnosis(
        source_c
    )

    source_c = enrich_diagnosis(
        source_c,
        dictionary
    )

    source_c = remove_duplicate_diagnoses(
        source_c
    )

    # Combine
    combined = combine_sources(
        source_a,
        source_b,
        source_c
    )

    rows_in = len(combined)

    combined, dropped = remove_duplicates(
        combined
    )

    tracker.add_stage(
        "Final grain deduplication",
        rows_in,
        len(combined),
        dropped,
        {
            "duplicate_source_claim_diagnosis": dropped
        }
    )

    final_output = prepare_final_output(
        combined
    )

    return final_output, tracker