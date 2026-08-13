import pandas as pd


START_DATE = pd.Timestamp("2018-01-01")
END_DATE = pd.Timestamp("2025-02-28")


def validate_output(df):
    results = {}

    # 1. Total rows
    total_rows = len(df)

    results["total_rows"] = {
        "passed": total_rows == 159704,
        "actual": total_rows,
        "expected": 159704
    }

    # 2. Distinct claims
    distinct_claims = df["CLAIM_ID"].nunique()

    results["distinct_claims"] = {
        "passed": distinct_claims == 68205,
        "actual": distinct_claims,
        "expected": 68205
    }

    # 3. Distinct patients
    distinct_patients = df["PATIENT_ID"].nunique()

    results["distinct_patients"] = {
        "passed": distinct_patients == 11963,
        "actual": distinct_patients,
        "expected": 11963
    }

    # 4. Distinct diagnosis codes
    distinct_codes = df["DIAGNOSIS_CODE"].nunique()

    results["distinct_diagnosis_codes"] = {
        "passed": distinct_codes == 44,
        "actual": distinct_codes,
        "expected": 44
    }

    # 5. P00042 - distinct diagnosis codes
    patient = df[df["PATIENT_ID"] == "P00042"]

    patient_codes = patient["DIAGNOSIS_CODE"].nunique()

    results["P00042_distinct_diagnosis_codes"] = {
        "passed": patient_codes == 7,
        "actual": patient_codes,
        "expected": 7
    }

    # 6. P00042 - total rows
    patient_rows = len(patient)

    results["P00042_total_rows"] = {
        "passed": patient_rows == 7,
        "actual": patient_rows,
        "expected": 7
    }

    # 7. Diagnosis codes have no dots and are uppercase
    codes_valid = (
        df["DIAGNOSIS_CODE"].notna()
        & ~df["DIAGNOSIS_CODE"].str.contains(
            ".",
            regex=False
        )
        & (
            df["DIAGNOSIS_CODE"]
            == df["DIAGNOSIS_CODE"].str.upper()
        )
    )

    results["diagnosis_codes_valid"] = {
        "passed": bool(codes_valid.all()),
        "actual_invalid_rows": int((~codes_valid).sum()),
        "expected": True
    }

    # 8. Service dates within required range
    dates_valid = df["SERVICE_DATE"].between(
        START_DATE,
        END_DATE
    )

    results["service_dates_valid"] = {
        "passed": bool(dates_valid.all()),
        "actual_invalid_rows": int((~dates_valid).sum()),
        "expected": True
    }

    # 9. No empty patient IDs
    patient_ids_valid = (
        df["PATIENT_ID"].notna()
        & (
            df["PATIENT_ID"]
            .astype(str)
            .str.strip()
            != ""
        )
    )

    results["patient_ids_valid"] = {
        "passed": bool(patient_ids_valid.all()),
        "actual_invalid_rows": int(
            (~patient_ids_valid).sum()
        ),
        "expected": True
    }

    return results
def compare_outputs(first_output, second_output):
    import pandas as pd

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

    first = (
        first_output[columns]
        .sort_values(
            ["SRC", "CLAIM_ID", "DIAGNOSIS_CODE"]
        )
        .reset_index(drop=True)
    )

    second = (
        second_output[columns]
        .sort_values(
            ["SRC", "CLAIM_ID", "DIAGNOSIS_CODE"]
        )
        .reset_index(drop=True)
    )

    try:
        pd.testing.assert_frame_equal(
            first,
            second,
            check_dtype=False
        )

        return True

    except AssertionError:
        return False        

def validate_deterministic_run(first_output, run_pipeline):
    second_output, _ = run_pipeline()

    passed = compare_outputs(
        first_output,
        second_output
    )

    return {
        "passed": passed,
        "actual": passed,
        "expected": True
    }
        
