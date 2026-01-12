import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="data/plants.db"):
        self.db_path = db_path
        self._create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')

        # Plants Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants (
                plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                species TEXT,
                type TEXT,
                planting_date DATE,
                last_watering DATE,
                last_fertilizing DATE,
                photo_url TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # Watering Schedule Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watering_schedules (
                schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER,
                frequency INTEGER, -- in days
                next_date DATE,
                amount TEXT,
                FOREIGN KEY (plant_id) REFERENCES plants (plant_id) ON DELETE CASCADE
            )
        ''')

        # Fertilizing Schedule Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fertilizing_schedules (
                schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER,
                frequency INTEGER, -- in days
                next_date DATE,
                fertilizer_type TEXT,
                FOREIGN KEY (plant_id) REFERENCES plants (plant_id) ON DELETE CASCADE
            )
        ''')

        # Care History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS care_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_id INTEGER,
                care_type TEXT, -- 'watering' or 'fertilizing'
                date DATE,
                notes TEXT,
                FOREIGN KEY (plant_id) REFERENCES plants (plant_id) ON DELETE CASCADE
            )
        ''')
        
        # Care History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT, 
                date DATE,
                status TEXT, -- 'unread', 'read'
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

# Global instance for easy access
db_path = os.path.join(os.getcwd(), 'data', 'plants.db')
# Ensure directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)
db = DatabaseManager(db_path)

