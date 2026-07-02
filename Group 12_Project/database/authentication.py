from tkinter import messagebox
from database.database import Database

class Authentication:
    def __init__(self):
        self.db = Database()

    def login(self, user_id, password, role):
        conn = self.db.connect()

        if conn is None:
            messagebox.showerror("Error", "Cannot connect to database!")
            return None

        cursor = conn.cursor()

        try:
            accounts = [
                ("Student", "Student", "studentID"),
                ("Lecturer", "Lecturer", "lecturerID"),
                ("Admin", "Admin", "adminID")
            ]

            for table, db_role, id_field in accounts:

                sql = f"""
                SELECT password
                FROM {table}
                WHERE {id_field} = ?
                """

                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()

                if result:

                    # Incorrect password
                    if result[0] != password:
                        conn.close()
                        messagebox.showerror(
                            "Login Failed",
                            "Incorrect ID or password."
                        )
                        return None

                    # Correct ID & password but wrong role
                    if db_role != role:
                        conn.close()
                        messagebox.showerror(
                            "Login Failed",
                            "Selected role does not match this account.\n"
                            "Please choose the correct role."
                        )
                        return None

                    # Login successful
                    conn.close()
                    return db_role

            conn.close()

            # ID not found
            messagebox.showerror(
                "Login Failed",
                "Incorrect ID or password."
            )
            return None

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
            return None
