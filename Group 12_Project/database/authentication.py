from tkinter import messagebox
from database import Database

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
                SELECT password, status
                FROM {table}
                WHERE {id_field} = ?
                """

                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()

                if result:
                    db_password = result[0]
                    status = result[1]

                    # Incorrect password
                    if db_password != password:
                        conn.close()
                        messagebox.showerror(
                            "Login Failed",
                            "Incorrect ID or password."
                        )
                        return None

                    # Account locked
                    if status == "Locked":
                        conn.close()
                        messagebox.showerror(
                            "Account Locked",
                            "Your account has been locked.\nPlease contact the administrator."
                        )
                        return None

                    # Correct ID & Password but wrong role
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
