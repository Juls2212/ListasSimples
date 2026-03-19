from taskModels import Task
from taskList import SinglyLinkedTaskList


class TaskService:
    def __init__(self):
        self.task_list = SinglyLinkedTaskList()
        self.next_id_number = 1

    def generate_task_id(self):
        generated_id = "T-" + str(self.next_id_number).zfill(3)
        self.next_id_number += 1
        return generated_id

    def validate_text(self, value, field_name):
        clean_value = value.strip()

        if clean_value == "":
            return False, field_name + " cannot be empty."

        return True, clean_value

    def create_task(self, title, description, priority):
        valid_title, title_result = self.validate_text(title, "Title")
        if not valid_title:
            return False, title_result, None

        valid_description, description_result = self.validate_text(description, "Description")
        if not valid_description:
            return False, description_result, None

        valid_priority, priority_result = self.validate_text(priority, "Priority")
        if not valid_priority:
            return False, priority_result, None

        new_task = Task(
            self.generate_task_id(),
            title_result,
            description_result,
            priority_result
        )

        self.task_list.insert_task(new_task)
        return True, "Task created successfully.", new_task

    def get_task_by_id(self, task_id):
        clean_id = task_id.strip()

        if clean_id == "":
            return None

        return self.task_list.find_task_by_id(clean_id)

    def update_task(self, task_id, title, description, priority):
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        valid_title, title_result = self.validate_text(title, "Title")
        if not valid_title:
            return False, title_result

        valid_description, description_result = self.validate_text(description, "Description")
        if not valid_description:
            return False, description_result

        valid_priority, priority_result = self.validate_text(priority, "Priority")
        if not valid_priority:
            return False, priority_result

        task.title = title_result
        task.description = description_result
        task.priority = priority_result

        return True, "Task updated successfully."

    def delete_task(self, task_id):
        clean_id = task_id.strip()

        if clean_id == "":
            return False, "Task ID is required."

        return self.task_list.delete_task(clean_id)

    def mark_task_completed(self, task_id):
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        task.status = "Completed"
        return True, "Task marked as completed."

    def mark_task_pending(self, task_id):
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        task.status = "Pending"
        return True, "Task marked as pending."

    def move_task_to_front(self, task_id):
        clean_id = task_id.strip()

        if clean_id == "":
            return False, "Task ID is required."

        return self.task_list.move_task_to_front(clean_id)

    def move_task_to_back(self, task_id):
        clean_id = task_id.strip()

        if clean_id == "":
            return False, "Task ID is required."

        return self.task_list.move_task_to_back(clean_id)

    def traverse_tasks(self, action):
        self.task_list.traverse_tasks(action)

    def get_statistics(self):
        total = self.task_list.count_all_tasks()
        pending = self.task_list.count_tasks_by_status("Pending")
        completed = self.task_list.count_tasks_by_status("Completed")

        return total, pending, completed