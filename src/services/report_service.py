from src.utils.database import db

class ReportService:
    def generate_report(self, user_id):
        """
        Generates a simple summary report for the user.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Total Plants
        cursor.execute("SELECT COUNT(*) FROM plants WHERE user_id = ?", (user_id,))
        total_plants = cursor.fetchone()[0]

        # Plants needing care
        cursor.execute('''
            SELECT COUNT(*) 
            FROM watering_schedules w
            JOIN plants p ON w.plant_id = p.plant_id
            WHERE p.user_id = ? AND w.next_date <= date('now')
        ''', (user_id,))
        plants_needing_water = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*) 
            FROM fertilizing_schedules f
            JOIN plants p ON f.plant_id = p.plant_id
            WHERE p.user_id = ? AND f.next_date <= date('now')
        ''', (user_id,))
        plants_needing_fertilizer = cursor.fetchone()[0]

        conn.close()

        report_content = f"""
        Plant Tracking Report
        ---------------------
        Total Plants: {total_plants}
        
        Action Items:
        - Plants needing water: {plants_needing_water}
        - Plants needing fertilizer: {plants_needing_fertilizer}
        """
        return report_content
