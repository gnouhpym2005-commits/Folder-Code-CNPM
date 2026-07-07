from database.database import Database


class PasswordRepository:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    def check_password(self, user_id, role, current_password):

        if role == "Student":
            table = "Student"
            field = "studentID"

        elif role == "Lecturer":
            table = "Lecturer"
            field = "lecturerID"

        else:
            table = "Admin"
            field = "adminID"

        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT password FROM {table} WHERE {field}=?",
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return False

        return row[0] == current_password
    
    def update_password(self, user_id, role, new_password):

        if role == "Student":
            table = "Student"
            field = "studentID"

        elif role == "Lecturer":
            table = "Lecturer"
            field = "lecturerID"

        else:
            table = "Admin"
            field = "adminID"

        sql = f"UPDATE {table} SET password=? WHERE {field}=?"

        cursor = self.conn.cursor()
        cursor.execute(sql, (new_password, user_id))

        self.conn.commit()