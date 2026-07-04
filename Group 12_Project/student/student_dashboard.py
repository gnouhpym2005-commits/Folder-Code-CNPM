import tkinter as tk
from tkinter import messagebox
from database.database import Database
from available_courses import AvailableCourses
from search_course import SearchCourse
from register_course import RegisterCourse
from my_courses import MyCourses
from timetable import TimeTable

class StudentDashboard:
    def __init__(self, student_id):

        self.student_id = student_id

        self.db = Database()
        self.conn = self.db.connect()

        self.root = tk.Tk()
        self.root.title("Student Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg="#F5F6FA")
        self.root.resizable(True, True)

        self.load_student()

        self.create_sidebar()

        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side="left", fill="both", expand=True)

        self.create_header()

        # Frame chứa nội dung các màn hình
        self.content_frame = tk.Frame(self.right_frame,bg="white")
        self.content_frame.pack(fill="both", expand=True)

        self.create_dashboard()

        self.root.mainloop()

    # Load Student
    def load_student(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT fullName,
               major,
               earnedCredits
        FROM Student
        WHERE studentID=?
        """, (self.student_id,))

        self.student = cursor.fetchone()

    # Sidebar
    def create_sidebar(self):
        sidebar = tk.Frame(
            self.root,
            bg="#F5F2E8",
            width=280
        )

        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Course Registration System",
            font=("Segoe UI", 14, "bold"),
            bg="#F5F2E8",
            anchor="w"
        ).pack(fill="x", padx=15,pady=20)

        menu = [
            ("🏠 Dashboard", self.open_dashboard),
            ("📚 Available Courses", self.open_available),
            ("🔍 Search Courses", self.open_search),
            ("📝 Register Courses", self.open_register),
            ("🎓 My Courses", self.open_mycourse),
            ("📅 Timetable", self.open_timetable)
        ]

        for text, command in menu:
            tk.Button(
                sidebar,
                text=text,
                font=("Segoe UI", 11),
                bg="#F5F2E8",
                relief="flat",
                anchor="w",
                padx=20,
                command=command
            ).pack(fill="x", pady=3)

        tk.Frame(
            sidebar,
            bg="#CFCFCF",
            height=1
        ).pack(fill="x", padx=15, pady=20)

        tk.Button(
            sidebar,
            text="🚪 Logout",
            font=("Segoe UI", 11),
            bg="#F5F2E8",
            relief="flat",
            anchor="w",
            padx=20,
            command=self.logout
        ).pack(fill="x")

    # Header
    def create_header(self):
        header = tk.Frame(
            self.right_frame,
            bg="#DCEEFF",
            height=60
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"👤 Student: {self.student.fullName}",
            bg="#DCEEFF",
            font=("Segoe UI", 11, "bold")
        ).pack(side="right", padx=20)

    # Dashboard
    def create_dashboard(self):
        body = tk.Frame( self.content_frame,bg="white")

        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text=f"Welcome, {self.student.fullName}",
            bg="white",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=30, pady=20)

        cards = tk.Frame(body, bg="white")
        cards.pack(pady=10)

        data = [
            (
                "📚",
                "Available Courses",
                "View all courses\navailable this semester",
                "#6C63FF",
                "View Courses",
                self.open_available
            ),

            (
                "📝",
                "Register Courses",
                "Register for your\ndesired courses",
                "#4CAF50",
                "Register Now",
                self.open_register
            ),

            (
                "📋",
                "My Courses",
                "View your registered\ncourses and schedule",
                "#E53935",
                "View",
                self.open_mycourse
            )

        ]

        for i, item in enumerate(data):
            icon, title, des, color, btn, cmd = item

            card = tk.Frame(
                cards,
                bg="white",
                width=220,
                height=180,
                relief="solid",
                bd=1
            )

            card.grid(row=0, column=i, padx=12)

            card.pack_propagate(False)

            tk.Label(
                card,
                text=icon,
                font=("Segoe UI", 18),
                bg="white"
            ).pack(pady=(15, 5))

            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 11, "bold"),
                bg="white"
            ).pack()

            tk.Label(
                card,
                text=des,
                font=("Segoe UI", 9),
                fg="gray",
                bg="white",
                justify="center"
            ).pack(pady=10)

            tk.Button(
                card,
                text=btn,
                bg=color,
                fg="white",
                relief="flat",
                width=15,
                command=cmd
            ).pack()

        tk.Label(
            body,
            text="Important Information",
            font=("Segoe UI", 13, "bold"),
            bg="white"
        ).pack(anchor="w", padx=30, pady=(35, 10))

        notice = tk.Frame(
            body,
            bg="#FFF59D",
            height=90
        )

        notice.pack(fill="x", padx=30)
        notice.pack_propagate(False)

        tk.Label(
            notice,
            text="🔔",
            font=("Segoe UI", 24),
            bg="#FFF59D"
        ).pack(side="left", padx=20)

        info = tk.Frame(
            notice,
            bg="#FFF59D"
        )

        info.pack(side="left", pady=12)

        tk.Label(
            info,
            text="• Course registration period: 15/05/2026 - 30/05/2026",
            bg="#FFF59D",
            font=("Segoe UI", 11)
        ).pack(anchor="w")

        tk.Label(
            info,
            text="• Make sure to check your timetable for any schedule conflicts",
            bg="#FFF59D",
            font=("Segoe UI", 11)
        ).pack(anchor="w")

    # Navigation
    def open_dashboard(self):
        self.clear_content()
        self.create_dashboard()

    def open_available(self):
        self.clear_content()
        AvailableCourses(self.content_frame, self.student_id)

    def open_search(self):
        self.clear_content()
        SearchCourse(self.content_frame, self.student_id)

    def open_register(self):
        self.clear_content()
        RegisterCourse(self.content_frame, self.student_id)

    def open_mycourse(self):
        self.clear_content()
        MyCourses(self.content_frame, self.student_id)

    def open_timetable(self):
        self.clear_content()
        TimeTable(self.content_frame, self.student_id)

    def logout(self):
        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        )

        if answer:
            self.root.destroy()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
