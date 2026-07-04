import tkinter as tk
from tkinter import ttk, messagebox
from database.database import Database

class AvailableCourses:
    def __init__(self, parent, student_id):

        self.parent = parent
        self.student_id = student_id

        self.db = Database()
        self.conn = self.db.connect()

        self.window = tk.Frame(self.parent, bg="white")
        self.window.pack(fill="both", expand=True)

        self.create_widgets()
        self.load_courses()

    # UI
    def create_widgets(self):
        # ---------------- Main ----------------
        body = tk.Frame(self.window, bg="white")

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            body,
            text="Available Courses",
            bg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        # Search
        self.search_entry = tk.Entry(
            body,
            font=("Segoe UI", 11),
            width=40
        )

        self.search_entry.pack(anchor="w", pady=15)

        self.search_entry.insert(0, "Search course by name or code...")

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_course
        )

        # ---------------- Table ----------------
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        columns = (
            "Code",
            "Course Name",
            "Credits",
            "Lecturer",
            "Room",
            "Schedule",
            "Available Seats"
        )

        table_frame = tk.Frame(body, bg="white")

        table_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame)

        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=10
        )

        scrollbar.config(command=self.tree.yview)

        widths = [90, 240, 70, 170, 90, 120, 120]

        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)

            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # ---------------- Bottom ----------------
        bottom = tk.Frame(body, bg="white")

        bottom.pack(fill="x", pady=10)

        self.total_label = tk.Label(
            bottom,
            text="Total: 0 courses",
            bg="white",
            font=("Segoe UI", 10)
        )

        self.total_label.pack(side="left")

        tk.Button(
            bottom,
            text="View Detail",
            bg="#6C63FF",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10),
            command=self.view_detail
        ).pack(side="right", padx=5)

        tk.Button(
            bottom,
            text="Refresh",
            bg="#4CAF50",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10),
            command=self.load_courses
        ).pack(side="right", padx=5)

        tk.Button(
            bottom,
            text="Close",
            bg="#E53935",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10),
            command=self.window.destroy
        ).pack(side="right", padx=5)

    # Load Courses
    def load_courses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName,
                s.credits,
                l.fullName,
                cc.room,
                cc.dayOfWeek,
                cc.currentEnrolled,
                cc.maxCapacity
            FROM CourseClass cc
            
            JOIN Subject s ON cc.subjectID=s.subjectID

            JOIN Lecturer l ON cc.lecturerID=l.lecturerID

            JOIN RegistrationPeriod rp ON cc.periodID=rp.periodID

            WHERE rp.status='Open' AND cc.status='Open'
        """)

        rows = cursor.fetchall()

        self.total_label.config(text=f"Total: {len(rows)} courses")

        for row in rows:
            available = row.maxCapacity - row.currentEnrolled
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.classID,
                    row.subjectName,
                    row.credits,
                    row.fullName,
                    row.room,
                    row.dayOfWeek,
                    available
                )
            )

    # Search Course
    def search_course(self, event):
        keyword = self.search_entry.get().strip().lower()

        # Hiển thị lại tất cả nếu ô tìm kiếm rỗng
        if keyword == "":
            for item in self.tree.get_children(""):
                self.tree.reattach(item, "", "end")
            return

        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]

            text = " ".join(map(str, values)).lower()

            if keyword in text:
                self.tree.reattach(item, "", "end")
            else:
                self.tree.detach(item)

    # View Detail
    def view_detail(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a course."
            )
            return

        class_id = self.tree.item(selected)["values"][0]

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                s.subjectID,
                s.subjectName,
                s.credits,
                s.department,
                s.description,
                l.fullName,
                cc.room,
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime,
                cc.currentEnrolled,
                cc.maxCapacity
            FROM CourseClass cc
                       
            JOIN Subject s ON cc.subjectID = s.subjectID

            JOIN Lecturer l ON cc.lecturerID = l.lecturerID

            WHERE cc.classID = ?
                       
        """, class_id)

        course = cursor.fetchone()

        if not course:
            messagebox.showerror(
                "Error",
                "Course not found."
            )
            return

        detail = tk.Toplevel(self.window)

        detail.title("Course Detail")

        detail.geometry("500x520")

        detail.configure(bg="white")

        tk.Label(
            detail,
            text="Course Detail",
            font=("Segoe UI", 18, "bold"),
            bg="white"
        ).pack(pady=15)

        info_frame = tk.Frame(
            detail,
            bg="white"
        )

        info_frame.pack(fill="both", expand=True, padx=25)

        infos = [
            ("Subject ID", course.subjectID),
            ("Subject Name", course.subjectName),
            ("Credits", course.credits),
            ("Department", course.department),
            ("Lecturer", course.fullName),
            ("Room", course.room),
            ("Schedule", course.dayOfWeek),
            ("Time", f"{course.startTime} - {course.endTime}"),
            ("Seats", f"{course.currentEnrolled}/{course.maxCapacity}")
        ]

        for title, value in infos:
            row = tk.Frame(
                info_frame,
                bg="white"
            )

            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=title + ":",
                width=15,
                anchor="w",
                bg="white",
                font=("Segoe UI", 10, "bold")
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                bg="white",
                font=("Segoe UI", 10)
            ).pack(side="left")

        tk.Label(
            info_frame,
            text="Description",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(15, 5))

        description = tk.Text(
            info_frame,
            height=8,
            wrap="word",
            font=("Segoe UI", 10)
        )

        description.pack(fill="x")

        description.insert("1.0", course.description)

        description.config(state="disabled")

        tk.Button(
            detail,
            text="Close",
            bg="#E53935",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI", 10),
            command=detail.destroy
        ).pack(pady=20)
