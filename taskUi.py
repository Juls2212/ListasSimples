import tkinter as tk
from tkinter import ttk


class TaskForm(ttk.Frame):
    def __init__(self, master, callbacks):
        super().__init__(master, style="Card.TFrame", padding=18)
        self.callbacks = callbacks
        self.build_form()

    def build_form(self):
        ttk.Label(self, text="Task Form", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Label(self, text="Task ID", style="FieldLabel.TLabel").pack(anchor="w")
        self.id_entry = ttk.Entry(self, width=34)
        self.id_entry.pack(fill="x", pady=(4, 12))

        ttk.Label(self, text="Title", style="FieldLabel.TLabel").pack(anchor="w")
        self.title_entry = ttk.Entry(self, width=34)
        self.title_entry.pack(fill="x", pady=(4, 12))

        ttk.Label(self, text="Description", style="FieldLabel.TLabel").pack(anchor="w")
        self.description_text = tk.Text(
            self,
            height=7,
            width=34,
            font=("Segoe UI", 10),
            wrap="word",
            relief="solid",
            bd=1
        )
        self.description_text.pack(fill="x", pady=(4, 12))

        ttk.Label(self, text="Priority", style="FieldLabel.TLabel").pack(anchor="w")
        self.priority_combo = ttk.Combobox(
            self,
            state="readonly",
            values=("High", "Medium", "Low"),
            width=31
        )
        self.priority_combo.pack(fill="x", pady=(4, 16))
        self.priority_combo.set("Medium")

        ttk.Button(self, text="Add Task", command=self.callbacks["add"]).pack(fill="x", pady=4)
        ttk.Button(self, text="Update Task", command=self.callbacks["update"]).pack(fill="x", pady=4)
        ttk.Button(self, text="Clear Form", command=self.callbacks["clear"]).pack(fill="x", pady=4)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=14)

        ttk.Label(self, text="Task Actions", style="SectionTitle.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Button(self, text="Search by ID", command=self.callbacks["search"]).pack(fill="x", pady=4)
        ttk.Button(self, text="Mark Completed", command=self.callbacks["complete"]).pack(fill="x", pady=4)
        ttk.Button(self, text="Mark Pending", command=self.callbacks["pending"]).pack(fill="x", pady=4)
        ttk.Button(self, text="Move to Front", command=self.callbacks["front"]).pack(fill="x", pady=4)
        ttk.Button(self, text="Move to Back", command=self.callbacks["back"]).pack(fill="x", pady=4)
        ttk.Button(self, text="Delete Task", command=self.callbacks["delete"]).pack(fill="x", pady=4)

    def get_form_data(self):
        task_id = self.id_entry.get().strip()
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", "end").strip()
        priority = self.priority_combo.get().strip()

        return task_id, title, description, priority

    def get_task_id(self):
        return self.id_entry.get().strip()

    def set_form_data(self, task):
        self.id_entry.delete(0, "end")
        self.id_entry.insert(0, task.task_id)

        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, task.title)

        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", task.description)

        self.priority_combo.set(task.priority)

    def clear_form(self):
        self.id_entry.delete(0, "end")
        self.title_entry.delete(0, "end")
        self.description_text.delete("1.0", "end")
        self.priority_combo.set("Medium")


class TaskTable(ttk.Frame):
    def __init__(self, master, on_select):
        super().__init__(master, style="Card.TFrame", padding=18)
        self.on_select = on_select
        self.build_table()

    def build_table(self):
        ttk.Label(self, text="Task List", style="SectionTitle.TLabel").pack(anchor="w")

        self.summary_label = ttk.Label(
            self,
            text="Total: 0 | Pending: 0 | Completed: 0",
            style="Summary.TLabel"
        )
        self.summary_label.pack(anchor="w", pady=(6, 12))

        columns = ("id", "title", "priority", "status", "description")

        table_container = tk.Frame(self, bg="#ffffff")
        table_container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("status", text="Status")
        self.tree.heading("description", text="Description")

        self.tree.column("id", width=90, anchor="center")
        self.tree.column("title", width=220, anchor="w")
        self.tree.column("priority", width=100, anchor="center")
        self.tree.column("status", width=120, anchor="center")
        self.tree.column("description", width=380, anchor="w")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.handle_select)

    def handle_select(self, event):
        self.on_select()

    def refresh_table(self, service):
        existing_items = self.tree.get_children()

        for item in existing_items:
            self.tree.delete(item)

        def insert_row(task):
            self.tree.insert(
                "",
                "end",
                values=(
                    task.task_id,
                    task.title,
                    task.priority,
                    task.status,
                    task.description
                )
            )

        service.traverse_tasks(insert_row)

        total, pending, completed = service.get_statistics()
        self.summary_label.config(
            text="Total: " + str(total) +
                 " | Pending: " + str(pending) +
                 " | Completed: " + str(completed)
        )

    def get_selected_task_id(self):
        selection = self.tree.selection()

        if not selection:
            return ""

        item_values = self.tree.item(selection[0], "values")

        if not item_values:
            return ""

        return item_values[0]

    def select_task_by_id(self, task_id):
        items = self.tree.get_children()

        for item in items:
            values = self.tree.item(item, "values")

            if values and values[0] == task_id:
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                return True

        return False

    def clear_selection(self):
        selected_items = self.tree.selection()

        for item in selected_items:
            self.tree.selection_remove(item)