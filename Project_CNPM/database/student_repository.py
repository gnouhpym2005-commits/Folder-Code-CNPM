from database.database import Database


class StudentRepository:

    def __init__(self):
        self.db = Database()

    # ==========================
    # Load all students
    # ==========================
    def get_all(self):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                studentID,
                fullName,
                major,
                status
            FROM Student
            ORDER BY studentID
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows

    # ==========================
    # Add Student
    # ==========================
    def insert(self, studentID, fullName, major, status):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Student
            (
                studentID,
                fullName,
                major,
                status
            )
            VALUES
            (
                ?, ?, ?, ?
            )
        """,
        (
            studentID,
            fullName,
            major,
            status
        ))

        conn.commit()
        conn.close()

    # ==========================
    # Update Student
    # ==========================
    def update(self, studentID, fullName, major, status):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Student
            SET
                fullName=?,
                major=?,
                status=?
            WHERE studentID=?
        """,
        (
            fullName,
            major,
            status,
            studentID
        ))

        conn.commit()
        conn.close()

    # ==========================
    # Change Status
    # ==========================
    def change_status(self, studentID, status):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Student
            SET status=?
            WHERE studentID=?
        """,
        (
            status,
            studentID
        ))

        conn.commit()
        conn.close()
