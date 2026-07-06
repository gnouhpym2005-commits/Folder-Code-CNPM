from database.database import Database

class CourseRepository:
    def __init__(self):
        self.db = Database()
    def get_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                subjectID,
                subjectName,
                credits
            FROM Subject
            ORDER BY subjectID
        """)
        data = cursor.fetchall()
        conn.close()
        return data