import pandas as pd

df = pd.read_excel("data/source_c_claims.csv.xlsx")

print(
    df[df["claim_ref"] == "C9000000"][
        [
            "claim_ref",
            "version",
            "seq",
            "date_of_service",
            "diagnosis_codes"
        ]
    ].sort_values(["version", "seq"]).to_string(index=False)
)
print(
    df[df["pt_ref"] == "P00042"][
        [
            "pt_ref",
            "claim_ref",
            "version",
            "seq",
            "date_of_service",
            "diagnosis_codes"
        ]
    ].sort_values(["claim_ref", "version", "seq"]).to_string(index=False)
)