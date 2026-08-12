import pandas as pd

from pipeline.pipeline import run_pipeline


def test_two_runs_are_identical():
    output_1, _ = run_pipeline()
    output_2, _ = run_pipeline()

    output_1 = output_1.sort_values(
        [
            "SRC",
            "CLAIM_ID",
            "DIAGNOSIS_CODE"
        ]
    ).reset_index(drop=True)

    output_2 = output_2.sort_values(
        [
            "SRC",
            "CLAIM_ID",
            "DIAGNOSIS_CODE"
        ]
    ).reset_index(drop=True)

    pd.testing.assert_frame_equal(
        output_1,
        output_2,
        check_dtype=False
    )