class User:
    def __init__(self, user_id=None, name="", surname="", email="", password="", role="user"):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.role = role

    @staticmethod
    def from_row(row):
        return User(
            user_id=row[0],
            name=row[1],
            surname=row[2],
            email=row[3],
            password=row[4],
            role=row[5]
        )
