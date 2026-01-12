from src.utils.database import db
from src.models.user import User

class AuthService:
    def login(self, email, password):
        """
        Authenticates a user.
        Returns the User object if successful, None otherwise.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User.from_row(row)
        return None

    def register(self, name, surname, email, password):
        """
        Registers a new user.
        Returns the new User object if successful, raises Exception if email exists.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (name, surname, email, password) VALUES (?, ?, ?, ?)", 
                           (name, surname, email, password))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return User(user_id, name, surname, email, password)
        except Exception as e:
            conn.close()
            print(f"Registration error: {e}")
            return None
