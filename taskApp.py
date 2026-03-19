import tkinter as tk
from tkinter import ttk, messagebox

from taskUi import TaskForm, TaskTable


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
            text="All task operations work with nodes and next references.",
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
        self.table.refresh_table(self.service)

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
        self.table.select_task_by_id(task.task_id)

    def update_task(self):
        task_id, title, description, priority = self.form.get_form_data()

        if task_id == "":
            messagebox.showwarning("Validation", "Task ID is required.")
            return

        success, message = self.service.update_task(task_id, title, description, priority)

        if success:
            messagebox.showinfo("Success", message)
            self.refresh_table()
            self.table.select_task_by_id(task_id)
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
        self.table.select_task_by_id(task_id)

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
            self.table.select_task_by_id(task_id)
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
            self.table.select_task_by_id(task_id)
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
            self.table.select_task_by_id(task_id)
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
            self.table.select_task_by_id(task_id)
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