def enrich_diagnosis(df, dictionary):
    df = df.copy()
    dictionary = dictionary.copy()

    dictionary["dx_code"] = (
        dictionary["dx_code"]
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(".", "", regex=False)
    )

    lookup = dict(
        zip(
            dictionary["dx_code"],
            dictionary["dx_description"]
        )
    )

    df["DIAGNOSIS_DESC"] = (
        df["DIAGNOSIS_CODE"]
        .map(lookup)
        .fillna("UNKNOWN")
    )

    return df