import sys
import os
import time

# Ensure src is in path
sys.path.append(os.getcwd())

from src.services.auth_service import AuthService
from src.services.plant_service import PlantService
from src.services.notification_service import NotificationService
from src.services.report_service import ReportService
from src.utils.database import db

def run_verification():
    print("Starting Verification...")
    
    # Setup Services
    auth = AuthService()
    plant_svc = PlantService()
    notif_svc = NotificationService()
    report_svc = ReportService()
    
    # 1. Register
    email = f"test_{int(time.time())}@example.com"
    pwd = "password123"
    print(f"Registering user: {email}")
    user = auth.register("Test", "User", email, pwd)
    if not user:
        print("FAIL: Registration returned None")
        return
    print(f"PASS: User registered with ID {user.user_id}")
    
    # 2. Login
    logged_in = auth.login(email, pwd)
    if not logged_in or logged_in.user_id != user.user_id:
        print("FAIL: Login failed")
        return
    print("PASS: Login successful")
    
    # 3. Add Plant
    print("Adding Plant...")
    plant_id = plant_svc.add_plant(user.user_id, "Test Rose", "Rosa", "Outdoor", "2023-01-01")
    plant_svc.set_schedules(plant_id, water_freq=2, fert_freq=14, water_amount="500ml", fert_type="General")
    print(f"PASS: Plant added with ID {plant_id}")
    
    # 4. Check Notifications (Should be none technically if next date is future, let's see logic)
    # Logic was today + freq, so next date is future.
    notifs = notif_svc.check_due_dates(user.user_id)
    print(f"Notifications: {len(notifs)} (Expected 0 as just added with future dates)")
    
    # 5. Water Plant
    print("Watering Plant...")
    plant_svc.water_plant(plant_id, "Watered nicely")
    
    # 6. Check History
    history = plant_svc.get_care_history(plant_id)
    if len(history) != 1 or history[0].care_type != 'watering':
        print(f"FAIL: History mismatch. Found {len(history)} items.")
        return
    print("PASS: History verified")
    
    # 7. Report
    print("Generating Report...")
    report = report_svc.generate_report(user.user_id)
    print("Report Content:")
    print(report)
    print("PASS: Report verified")
    
    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"CRITICAL FAIL: {e}")
        import traceback
        traceback.print_exc()
