def standardize_source_a(df):
    df = df.rename(columns={
        "patient_id": "PATIENT_ID",
        "claim_id": "CLAIM_ID",
        "service_from_date": "SERVICE_DATE",
        "patient_birth_year": "BIRTH_YEAR",
        "patient_gender": "GENDER",
        "patient_zip3": "ZIP3",
        "place_of_svc_cd": "PLACE_OF_SERVICE",
        "provider_rendering_id": "RENDERING_NPI",
        "provider_referring_id": "REFERRING_NPI",
        "provider_billing_id": "BILLING_NPI",
        "primary_plan_id": "PRIMARY_PLAN_ID",
        "bill_amt": "BILLED_AMOUNT",
        "data_source": "SRC"
    })

    return df


def standardize_source_b(df):
    df = df.rename(columns={
        "member_id": "PATIENT_ID",
        "encounter_id": "CLAIM_ID",
        "svc_date": "SERVICE_DATE",
        "birth_yr": "BIRTH_YEAR",
        "gender": "GENDER",
        "zip3": "ZIP3",
        "pos_code": "PLACE_OF_SERVICE",
        "rendering_npi": "RENDERING_NPI",
        "referring_npi": "REFERRING_NPI",
        "billing_npi": "BILLING_NPI",
        "payer_primary": "PRIMARY_PLAN_ID",
        "billed_amount": "BILLED_AMOUNT",
        "src": "SRC"
    })

    return df


def standardize_source_c(df):
    df = df.rename(columns={
        "pt_ref": "PATIENT_ID",
        "claim_ref": "CLAIM_ID",
        "date_of_service": "SERVICE_DATE",
        "yob": "BIRTH_YEAR",
        "sex": "GENDER",
        "zip_3": "ZIP3",
        "service_place": "PLACE_OF_SERVICE",
        "npi_rendering": "RENDERING_NPI",
        "npi_referring": "REFERRING_NPI",
        "npi_billing": "BILLING_NPI",
        "plan_1": "PRIMARY_PLAN_ID",
        "amount_billed": "BILLED_AMOUNT",
        "source_system": "SRC"
    })

    return df