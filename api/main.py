from fastapi import FastAPI
from uuid import uuid4

from pipeline.pipeline import run_pipeline
from pipeline.validation import (
    validate_output,
    validate_deterministic_run
)


app = FastAPI(
    title="Claims Data Harmonization API"
)


runs = {}


@app.post("/run")
def create_run():
    run_id = str(uuid4())

    output, tracker = run_pipeline()

    runs[run_id] = {
        "output": output,
        "stages": tracker.get_stages()
    }

    return {
        "run_id": run_id
    }


@app.get("/run/{run_id}/stages")
def get_stages(run_id: str):

    if run_id not in runs:
        return {
            "error": "Run not found"
        }

    return {
        "run_id": run_id,
        "stages": runs[run_id]["stages"]
    }


@app.get("/run/{run_id}/validate")
def validate_run(run_id: str):

    if run_id not in runs:
        return {
            "error": "Run not found"
        }

    output = runs[run_id]["output"]

    results = validate_output(output)

    deterministic = validate_deterministic_run(
        run_pipeline
    )

    results["deterministic_output"] = deterministic

    return {
        "run_id": run_id,
        "checks": results
    }


@app.get("/summary")
def get_summary():

    summaries = []

    for run_id, run in runs.items():

        output = run["output"]

        summaries.append({
            "run_id": run_id,
            "rows": len(output),
            "claims": output["CLAIM_ID"].nunique(),
            "patients": output["PATIENT_ID"].nunique(),
            "diagnosis_codes": output["DIAGNOSIS_CODE"].nunique()
        })

    return {
        "runs": summaries
    }