class Task:
    def __init__(self, task_id, title, description, priority):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "Pending"


class TaskNode:
    def __init__(self, task):
        self.task = task
        self.next = None