import tkinter as tk
from tkinter import ttk, messagebox
from database.lecturer_repository import LecturerRepository

class ManageLecturersApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        tk.Label(self.parent, text="MANAGE LECTURER", font=("Arial", 16, "bold"), bg="#f4f6f9").pack(pady=10)

        form_frame = tk.LabelFrame(self.parent, text="Lecturer Information", font=("Arial", 10), bg="#f4f6f9", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        form_frame.columnconfigure(0, minsize=120)
        form_frame.columnconfigure(1, minsize=300)
        form_frame.columnconfigure(2, minsize=120)
        form_frame.columnconfigure(3, minsize=300)

        tk.Label(form_frame, text="Lecturer ID:", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_id = ttk.Entry(form_frame, width=35)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Lecturer Name:", bg="#f4f6f9").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_name = ttk.Entry(form_frame, width=35)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Department:", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cbo_dept = ttk.Entry(form_frame, width=35)
        self.cbo_dept.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Status:", bg="#f4f6f9").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.cbo_status = ttk.Combobox(form_frame, values=["Active", "Locked"], width=35)
        self.cbo_status.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        btn_frame = tk.Frame(self.parent, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            btn_frame,
            text="Add",
            bg="#2ecc71",
            fg="white",
            width=15,
            command=self.add_lecturer
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Edit",
            bg="#f39c12",
            fg="white",
            width=15,
            command=self.edit_lecturer
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Lock/Unlock",
            bg="#e74c3c",
            fg="white",
            width=15,
            command=self.lock_unlock
        ).pack(side=tk.LEFT, padx=5)

        columns = ("id", "name", "dept", "status")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="Lecturer ID")
        self.tree.heading("name", text="FullName")
        self.tree.heading("dept", text="Department")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        self.repo = LecturerRepository()
        self.load_lecturers()

    def select_item(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected)["values"]
        # Lecturer ID
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, values[0])
        # Lecturer Name
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values[1])
        # Department
        self.cbo_dept.delete(0, tk.END)
        self.cbo_dept.insert(0, values[2])  
        # Status
        self.cbo_status.set(values[3])

    def load_lecturers(self):
        self.tree.delete(*self.tree.get_children())
        rows = self.repo.get_all()
        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=(row[0], row[1], row[2], row[3])
            )

    def add_lecturer(self):

        lecturer_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        department = self.cbo_dept.get()
        status = self.cbo_status.get()

        self.repo.add_lecturer(
            lecturer_id,
            name,
            "",
            "123456",
            department,
            "Lecturer",
            status
        )
        self.load_lecturers()

    def edit_lecturer(self):
        self.repo.update_lecturer(
            self.entry_id.get(),
            self.entry_name.get(),
            self.cbo_dept.get(),
            self.cbo_status.get()
        )
        self.load_lecturers()

    def lock_unlock(self):
        status = self.cbo_status.get()
        if status == "Active":
            self.repo.lock_lecturer(self.entry_id.get())
        else:
            self.repo.unlock_lecturer(self.entry_id.get())
        self.load_lecturers()