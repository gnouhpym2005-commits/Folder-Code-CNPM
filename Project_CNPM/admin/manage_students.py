import tkinter as tk
from tkinter import ttk, messagebox
from database.student_repository import StudentRepository

class ManageStudentsApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        tk.Label(self.parent, text="MANAGE STUDENTS", font=("Arial", 16, "bold"), bg="#f4f6f9").pack(pady=10)

        form_frame = tk.LabelFrame(self.parent, text="Thông tin Sinh viên", font=("Arial", 10), bg="#f4f6f9", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(form_frame, text="Student ID:", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_id = ttk.Entry(form_frame, width=20)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Fullname:", bg="#f4f6f9").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_name = ttk.Entry(form_frame, width=30)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Ngành học:", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cbo_major = ttk.Combobox(form_frame, values=["CNTT", "Kinh tế", "Ngôn ngữ Anh"], width=17)
        self.cbo_major.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Status:", bg="#f4f6f9").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.cbo_status = ttk.Combobox(form_frame, values=["ACTIVE", "LOCKED"], width=27)
        self.cbo_status.grid(row=1, column=3, padx=5, pady=5)

        btn_frame = tk.Frame(self.parent, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            btn_frame,
            text="Add",
            bg="#2ecc71",
            fg="white",
            width=15,
            command=self.add_student
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Edit",
            bg="#f39c12",
            fg="white",
            width=15,
            command=self.update_student
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Lock/Unclock",
            bg="#e74c3c",
            fg="white",
            width=15,
            command=self.change_status
        ).pack(side=tk.LEFT, padx=5)

        columns = ("id", "name", "major", "status")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="Student ID")
        self.tree.heading("name", text="Fullname")
        self.tree.heading("major", text="Major")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.select_student)

        self.repo = StudentRepository()
        self.load_students()

    def select_student(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, values[0])

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values[1])
        self.cbo_major.set(values[5])
        self.cbo_status.set(values[7])

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        students = self.repo.get_all()
        for s in students:
            self.tree.insert("", "end", values=(
                s.studentID,
                s.fullName,
                s.major,
                s.status
            ))
    def add_student(self):
        studentID = self.entry_id.get()
        fullName = self.entry_name.get()
        major = self.cbo_major.get()
        status = self.cbo_status.get()
        self.repo.insert(
            self.entry_id.get(),
            self.entry_name.get(),
            self.cbo_major.get(),
            self.cbo_status.get()
)
        self.load_students()

    def update_student(self):
        self.repo.update(
            self.entry_id.get(),
            self.entry_name.get(),
            self.cbo_major.get(),
            self.cbo_status.get()
        )
        self.load_students()

    def change_status(self):
        current = self.cbo_status.get()
        if current == "ACTIVE":
            new_status = "LOCKED"
        else:
            new_status = "ACTIVE"
        self.repo.change_status(
            self.entry_id.get(),
            new_status
        )
        self.load_students()