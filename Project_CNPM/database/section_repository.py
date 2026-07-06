from database.database import Database

class SectionRepository:
    def __init__(self):
        self.db = Database()
    def get_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                classID,
                subjectID,
                lecturerID,
                periodID,
                maxCapacity
            FROM CourseClass
            ORDER BY classID
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows