class WateringSchedule:
    def __init__(self, schedule_id=None, plant_id=None, frequency=1, next_date=None, amount=""):
        self.schedule_id = schedule_id
        self.plant_id = plant_id
        self.frequency = frequency
        self.next_date = next_date
        self.amount = amount

    @staticmethod
    def from_row(row):
        return WateringSchedule(
            schedule_id=row[0],
            plant_id=row[1],
            frequency=row[2],
            next_date=row[3],
            amount=row[4]
        )

class FertilizingSchedule:
    def __init__(self, schedule_id=None, plant_id=None, frequency=1, next_date=None, fertilizer_type=""):
        self.schedule_id = schedule_id
        self.plant_id = plant_id
        self.frequency = frequency
        self.next_date = next_date
        self.fertilizer_type = fertilizer_type

    @staticmethod
    def from_row(row):
        return FertilizingSchedule(
            schedule_id=row[0],
            plant_id=row[1],
            frequency=row[2],
            next_date=row[3],
            fertilizer_type=row[4]
        )
