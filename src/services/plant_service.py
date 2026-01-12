from src.utils.database import db
from src.models.plant import Plant
from src.models.schedule import WateringSchedule, FertilizingSchedule
from src.models.history import CareHistory
from datetime import datetime, timedelta

class PlantService:
    def get_plants_by_user(self, user_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plants WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Plant.from_row(row) for row in rows]

    def add_plant(self, user_id, name, species, type_, planting_date, photo_url=""):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO plants (user_id, name, species, type, planting_date, photo_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, name, species, type_, planting_date, photo_url))
        plant_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return plant_id

    def set_schedules(self, plant_id, water_freq, fert_freq, water_amount, fert_type):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Calculate next dates (assuming starting from today)
        today = datetime.now().date()
        next_water = today + timedelta(days=int(water_freq))
        next_fert = today + timedelta(days=int(fert_freq))

        # Watering Schedule
        cursor.execute('''
            INSERT INTO watering_schedules (plant_id, frequency, next_date, amount)
            VALUES (?, ?, ?, ?)
        ''', (plant_id, water_freq, next_water, water_amount))

        # Fertilizing Schedule
        cursor.execute('''
            INSERT INTO fertilizing_schedules (plant_id, frequency, next_date, fertilizer_type)
            VALUES (?, ?, ?, ?)
        ''', (plant_id, fert_freq, next_fert, fert_type))

        conn.commit()
        conn.close()

    def get_plant_details(self, plant_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM plants WHERE plant_id = ?", (plant_id,))
        plant_row = cursor.fetchone()
        plant = Plant.from_row(plant_row) if plant_row else None

        cursor.execute("SELECT * FROM watering_schedules WHERE plant_id = ?", (plant_id,))
        water_row = cursor.fetchone()
        water_schedule = WateringSchedule.from_row(water_row) if water_row else None

        cursor.execute("SELECT * FROM fertilizing_schedules WHERE plant_id = ?", (plant_id,))
        fert_row = cursor.fetchone()
        fert_schedule = FertilizingSchedule.from_row(fert_row) if fert_row else None

        conn.close()
        return plant, water_schedule, fert_schedule

    def water_plant(self, plant_id, notes=""):
        self._record_care(plant_id, 'watering', notes)
        self._update_schedule(plant_id, 'watering')

    def fertilize_plant(self, plant_id, notes=""):
        self._record_care(plant_id, 'fertilizing', notes)
        self._update_schedule(plant_id, 'fertilizing')

    def _record_care(self, plant_id, type_, notes):
        today = datetime.now().date()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO care_history (plant_id, care_type, date, notes)
            VALUES (?, ?, ?, ?)
        ''', (plant_id, type_, today, notes))
        
        # Update plant last care date
        if type_ == 'watering':
            cursor.execute("UPDATE plants SET last_watering = ? WHERE plant_id = ?", (today, plant_id))
        else:
            cursor.execute("UPDATE plants SET last_fertilizing = ? WHERE plant_id = ?", (today, plant_id))
            
        conn.commit()
        conn.close()

    def _update_schedule(self, plant_id, type_):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if type_ == 'watering':
            cursor.execute("SELECT frequency FROM watering_schedules WHERE plant_id = ?", (plant_id,))
            freq = cursor.fetchone()[0]
            next_date = datetime.now().date() + timedelta(days=freq)
            cursor.execute("UPDATE watering_schedules SET next_date = ? WHERE plant_id = ?", (next_date, plant_id))
        else:
            cursor.execute("SELECT frequency FROM fertilizing_schedules WHERE plant_id = ?", (plant_id,))
            freq = cursor.fetchone()[0]
            next_date = datetime.now().date() + timedelta(days=freq)
            cursor.execute("UPDATE fertilizing_schedules SET next_date = ? WHERE plant_id = ?", (next_date, plant_id))

        conn.commit()
        conn.close()

    def get_care_history(self, plant_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM care_history WHERE plant_id = ? ORDER BY date DESC", (plant_id,))
        rows = cursor.fetchall()
        conn.close()
        return [CareHistory.from_row(row) for row in rows]
