import tkinter as tk
from tkinter import ttk, messagebox
from database.course_repository import CourseRepository

class ManageCoursesApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        tk.Label(self.parent, text="MANAGE COURSE", font=("Arial", 16, "bold"), bg="#f4f6f9").pack(pady=10)

        form_frame = tk.LabelFrame(self.parent, text="Course Information", font=("Arial", 10), bg="#f4f6f9", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(form_frame, text="Course ID:", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_id = ttk.Entry(form_frame, width=15)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Course Name:", bg="#f4f6f9").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_name = ttk.Entry(form_frame, width=35)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Credit:", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_credits = ttk.Entry(form_frame, width=15)
        self.entry_credits.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self.parent, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Add", bg="#2ecc71", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit", bg="#f39c12", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", bg="#c0392b", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        columns = ("id", "name", "credits")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="Course ID")
        self.tree.heading("name", text="Course Name")
        self.tree.heading("credits", text="Credit")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.repo = CourseRepository()
        self.load_courses()

    def load_courses(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.repo.get_all():
            self.tree.insert("", "end", values=(
                row.subjectID,
                row.subjectName,
                row.credits
            ))
            