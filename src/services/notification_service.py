from src.utils.database import db
from datetime import datetime

class NotificationService:
    def check_due_dates(self, user_id):
        """
        Checks for plants that need watering or fertilizing for the given user.
        Returns a list of notification dictionaries.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        notifications = []

        # Check Watering
        cursor.execute('''
            SELECT p.name, w.next_date 
            FROM watering_schedules w
            JOIN plants p ON w.plant_id = p.plant_id
            WHERE p.user_id = ? AND w.next_date <= ?
        ''', (user_id, today))
        
        for name, next_date in cursor.fetchall():
            notifications.append({
                "type": "Watering",
                "message": f"{name} needs watering today!",
                "date": next_date
            })

        # Check Fertilizing
        cursor.execute('''
            SELECT p.name, f.next_date 
            FROM fertilizing_schedules f
            JOIN plants p ON f.plant_id = p.plant_id
            WHERE p.user_id = ? AND f.next_date <= ?
        ''', (user_id, today))

        for name, next_date in cursor.fetchall():
            notifications.append({
                "type": "Fertilizing",
                "message": f"{name} needs fertilizing today!",
                "date": next_date
            })

        conn.close()
        return notifications
