from pipeline.tracker import PipelineTracker


def test_tracker():
    tracker = PipelineTracker()

    tracker.add_stage(
        "Remove missing patients",
        100,
        90,
        10,
        {"missing_patient_id": 10}
    )

    stages = tracker.get_stages()

    assert len(stages) == 1
    assert stages[0]["stage"] == "Remove missing patients"
    assert stages[0]["rows_in"] == 100
    assert stages[0]["rows_out"] == 90
    assert stages[0]["dropped"] == 10
    assert stages[0]["reasons"]["missing_patient_id"] == 10