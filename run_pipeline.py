from pipeline.pipeline import run_pipeline


df, tracker = run_pipeline()

print("\nPipeline stages")
print("=" * 60)

for stage in tracker.get_stages():
    print(stage)

print("\nFinal rows:", len(df))

print("\nRows by source:")
print(df["SRC"].value_counts())

print("\nDistinct claims:")
print(df["CLAIM_ID"].nunique())

print("\nDistinct patients:")
print(df["PATIENT_ID"].nunique())

p00042 = df[df["PATIENT_ID"] == "P00042"]

print("\nP00042")
print("Total rows:", len(p00042))
print("Distinct diagnosis codes:", p00042["DIAGNOSIS_CODE"].nunique())

print(
    p00042[
        ["SRC", "CLAIM_ID", "DIAGNOSIS_CODE"]
    ].sort_values(
        ["SRC", "CLAIM_ID", "DIAGNOSIS_CODE"]
    ).to_string(index=False)
)