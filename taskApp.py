import tkinter as tk
from tkinter import ttk, messagebox


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

    def get_task_id(self):
        return self.id_entry.get().strip()


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

    def refresh(self, service):
        items = self.tree.get_children()

        for item in items:
            self.tree.delete(item)

        def insert_task(task):
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

        service.traverse_tasks(insert_task)

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

        item_data = self.tree.item(selection[0], "values")

        if not item_data:
            return ""

        return item_data[0]

    def clear_selection(self):
        selected_items = self.tree.selection()

        for item in selected_items:
            self.tree.selection_remove(item)


class TaskApp(tk.Tk):
    def __init__(self, service):
        super().__init__()
        self.service = service

        self.title("Task Manager - Singly Linked List")
        self.geometry("1200x700")
        self.minsize(1050, 650)
        self.configure(bg="#eef2f7")

        self.configure_styles()
        self.build_interface()
        self.refresh_table()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame", background="#ffffff")

        style.configure(
            "MainTitle.TLabel",
            background="#eef2f7",
            foreground="#1f2a44",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#eef2f7",
            foreground="#5b6b82",
            font=("Segoe UI", 10)
        )

        style.configure(
            "SectionTitle.TLabel",
            background="#ffffff",
            foreground="#1f2a44",
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "FieldLabel.TLabel",
            background="#ffffff",
            foreground="#1f2a44",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "Summary.TLabel",
            background="#ffffff",
            foreground="#1f2a44",
            font=("Segoe UI", 10)
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28
        )

    def build_interface(self):
        main_container = tk.Frame(self, bg="#eef2f7")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        header = tk.Frame(main_container, bg="#eef2f7")
        header.pack(fill="x", pady=(0, 15))

        ttk.Label(
            header,
            text="Task Manager with Singly Linked List",
            style="MainTitle.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Full task management using nodes and next references.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(4, 0))

        content = tk.Frame(main_container, bg="#eef2f7")
        content.pack(fill="both", expand=True)

        callbacks = {
            "add": self.add_task,
            "update": self.update_task,
            "clear": self.clear_form,
            "search": self.search_task,
            "complete": self.mark_completed,
            "pending": self.mark_pending,
            "front": self.move_to_front,
            "back": self.move_to_back,
            "delete": self.delete_task
        }

        self.form = TaskForm(content, callbacks)
        self.form.pack(side="left", fill="y", padx=(0, 10))

        self.table = TaskTable(content, self.load_selected_task)
        self.table.pack(side="right", fill="both", expand=True)

    def clear_form(self):
        self.form.clear_form()
        self.table.clear_selection()

    def refresh_table(self):
        self.table.refresh(self.service)

    def load_selected_task(self):
        task_id = self.table.get_selected_task_id()

        if task_id == "":
            return

        task = self.service.get_task_by_id(task_id)

        if task is None:
            return

        self.form.set_form_data(task)

    def add_task(self):
        _, title, description, priority = self.form.get_form_data()

        success, message, task = self.service.create_task(title, description, priority)

        if not success:
            messagebox.showwarning("Validation", message)
            return

        messagebox.showinfo("Success", message + "\nGenerated ID: " + task.task_id)
        self.clear_form()
        self.refresh_table()

    def update_task(self):
        task_id, title, description, priority = self.form.get_form_data()

        if task_id == "":
            messagebox.showwarning("Validation", "Task ID is required.")
            return

        success, message = self.service.update_task(task_id, title, description, priority)

        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", message)

    def search_task(self):
        task_id = self.form.get_task_id()

        if task_id == "":
            messagebox.showwarning("Validation", "Task ID is required.")
            return

        task = self.service.get_task_by_id(task_id)

        if task is None:
            messagebox.showwarning("Warning", "Task not found.")
            return

        self.form.set_form_data(task)

        messagebox.showinfo(
            "Task Found",
            "ID: " + task.task_id +
            "\nTitle: " + task.title +
            "\nStatus: " + task.status
        )

    def mark_completed(self):
        task_id = self.form.get_task_id()

        if task_id == "":
            messagebox.showwarning("Validation", "Task ID is required.")
            return

        success, message = self.service.mark_task_completed(task_id)

        if success:
            messagebox.showinfo("Success", message)
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", message)

    def mark_pending(self):
        task_id = self.form.get_task_id()

        if task_id == "":
            messagebox.showwarning("Validation", "Task ID is required.")
            return

        success, message = self.service.mark_task_pending(task_id)

        if success:
            messagebox.showinfo("Success", message)
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", message)

    def move_to_front(self):
        task_id = self.form.get_task_id()

        if task_id == "":
            messagebox.showwarning("Validation", "Task ID is required.")
            return

        success, message = self.service.move_task_to_front(task_id)

        if success:
            messagebox.showinfo("Result", message)
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", message)

    def move_to_back(self):
        task_id = self.form.get_task_id()

        if task_id == "":
            messagebox.showwarning("Validation", "Task ID is required.")
            return

        success, message = self.service.move_task_to_back(task_id)

        if success:
            messagebox.showinfo("Result", message)
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", message)

    def delete_task(self):
        task_id = self.form.get_task_id()

        if task_id == "":
            messagebox.showwarning("Validation", "Task ID is required.")
            return

        confirm = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to delete task " + task_id + "?"
        )

        if not confirm:
            return

        success, message = self.service.delete_task(task_id)

        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", message)