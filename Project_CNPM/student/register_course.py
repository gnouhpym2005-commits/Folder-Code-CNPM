import tkinter as tk
from tkinter import ttk, messagebox
from database.student_repository import StudentRepository
import uuid

class RegisterCourse:
    def __init__(self, parent, student_id):

        self.parent = parent
        self.student_id = student_id


        self.repository = StudentRepository() 


        self.window = tk.Frame(self.parent,bg="white")

        self.window.pack(fill="both",expand=True)

        self.window.configure(bg="#F5F6FA")

        self.create_widgets()

        self.load_courses()

    # UI
    def create_widgets(self):
        # ---------------- Body ----------------
        body = tk.Frame(self.window,bg="white")

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            body,
            text="Register Courses",
            bg="white",
            font=("Segoe UI",22,"bold")
        ).pack(anchor="w")

        # ---------------- Information ----------------
        notice = tk.Frame(
            body,
            bg="#DCEEFF",
            height=45
        )

        notice.pack(fill="x", pady=15)

        notice.pack_propagate(False)

        tk.Label(
            notice,
            text="ⓘ  Click the Register button to register for a course.",
            bg="#DCEEFF",
            font=("Segoe UI",10,"bold")
        ).pack(anchor="w", padx=15, pady=10)

        # ---------------- Table ----------------
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            font=("Segoe UI",10),
            rowheight=30
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI",10,"bold")
        )

        columns = (
            "Code",
            "Course Name",
            "Credits",
            "Available Seats"
        )

        table_frame = tk.Frame(body,bg="white")

        table_frame.pack(fill="both",expand=True)

        scrollbar = ttk.Scrollbar(table_frame)

        scrollbar.pack(side="right",fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8
        )

        scrollbar.config(command=self.tree.yview)

        widths = [120,350,100,150]

        for col, width in zip(columns, widths):
            self.tree.heading(col,text=col)

            self.tree.column(
                col,
                width=width,
                anchor="center"
            )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # ---------------- Bottom ----------------
        bottom = tk.Frame(
            body,
            bg="white"
        )

        bottom.pack(
            fill="x",
            pady=10
        )

        self.total_label = tk.Label(
            bottom,
            text="Total: 0 courses",
            bg="white",
            font=("Segoe UI",10)
        )

        self.total_label.pack(side="left")

        tk.Button(
            bottom,
            text="Register",
            bg="#6BCB77",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10,"bold"),
            command=self.register_course
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
        rows = self.repository.get_open_courses()
        self.total_label.config(
            text=f"Total: {len(rows)} courses"
        )
        for row in rows:
            available = row.maxCapacity - row.currentEnrolled
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.classID,
                    row.subjectName,
                    row.credits,
                    available
                )
            )

    # Register Course
    def register_course(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a course."
            )
            return

        class_id = self.tree.item(selected)["values"][0]

        if self.repository.check_registered(self.student_id, class_id):
            messagebox.showerror(
                "Error",
                "You have already registered this course."
            )
            return

        if not self.repository.check_available_seats(class_id):
            messagebox.showerror(
                "Error",
                "This class is full."
            )
            return

        if not self.repository.check_schedule(self.student_id, class_id):
            messagebox.showerror(
                "Error",
                "Schedule conflict detected."
            )
            return
        
        if not self.repository.check_prerequisite(self.student_id, class_id):
            messagebox.showerror(
                "Error",
                "Prerequisite course has not been completed."
            )
            return
        
        self.repository.register_course(self.student_id, class_id)

        messagebox.showinfo(
            "Success",
            "Course registration submitted successfully.\n\nStatus: Pending"
        )
        self.load_courses()