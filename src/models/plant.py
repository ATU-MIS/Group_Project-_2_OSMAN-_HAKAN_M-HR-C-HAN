class Plant:
    def __init__(self, plant_id=None, user_id=None, name="", species="", type_="", planting_date=None, last_watering=None, last_fertilizing=None, photo_url=""):
        self.plant_id = plant_id
        self.user_id = user_id
        self.name = name
        self.species = species
        self.type = type_
        self.planting_date = planting_date
        self.last_watering = last_watering
        self.last_fertilizing = last_fertilizing
        self.photo_url = photo_url

    @staticmethod
    def from_row(row):
        return Plant(
            plant_id=row[0],
            user_id=row[1],
            name=row[2],
            species=row[3],
            type_=row[4],
            planting_date=row[5],
            last_watering=row[6],
            last_fertilizing=row[7],
            photo_url=row[8]
        )
