class PipelineTracker:

    def __init__(self):
        self.stages = []

    def add_stage(self, name, rows_in, rows_out, dropped=0, reasons=None):
        self.stages.append({
            "stage": name,
            "rows_in": rows_in,
            "rows_out": rows_out,
            "dropped": dropped,
            "reasons": reasons or {}
        })

    def get_stages(self):
        return self.stages