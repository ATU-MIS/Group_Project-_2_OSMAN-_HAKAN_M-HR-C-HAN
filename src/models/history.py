class CareHistory:
    def __init__(self, history_id=None, plant_id=None, care_type="", date=None, notes=""):
        self.history_id = history_id
        self.plant_id = plant_id
        self.care_type = care_type
        self.date = date
        self.notes = notes

    @staticmethod
    def from_row(row):
        return CareHistory(
            history_id=row[0],
            plant_id=row[1],
            care_type=row[2],
            date=row[3],
            notes=row[4]
        )
