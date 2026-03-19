from taskModels import TaskNode


class SinglyLinkedTaskList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def insert_task(self, task):
        new_node = TaskNode(task)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        return new_node

    def find_previous_and_current(self, task_id):
        previous = None
        current = self.head

        while current is not None:
            if current.task.task_id == task_id:
                return previous, current
            previous = current
            current = current.next

        return None, None

    def find_task_by_id(self, task_id):
        current = self.head

        while current is not None:
            if current.task.task_id == task_id:
                return current.task
            current = current.next

        return None

    def delete_task(self, task_id):
        previous, current = self.find_previous_and_current(task_id)

        if current is None:
            return False, "Task not found."

        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next

        if current == self.tail:
            self.tail = previous

        current.next = None

        if self.head is None:
            self.tail = None

        return True, "Task deleted successfully."

    def move_task_to_front(self, task_id):
        if self.is_empty():
            return False, "The list is empty."

        if self.head == self.tail:
            return True, "There is only one task in the list."

        previous, current = self.find_previous_and_current(task_id)

        if current is None:
            return False, "Task not found."

        if previous is None:
            return True, "The task is already at the beginning."

        next_node = current.next
        previous.next = next_node

        if current == self.tail:
            self.tail = previous

        current.next = self.head
        self.head = current

        return True, "Task moved to the beginning."

    def move_task_to_back(self, task_id):
        if self.is_empty():
            return False, "The list is empty."

        if self.head == self.tail:
            return True, "There is only one task in the list."

        previous, current = self.find_previous_and_current(task_id)

        if current is None:
            return False, "Task not found."

        if current == self.tail:
            return True, "The task is already at the end."

        next_node = current.next

        if previous is None:
            self.head = next_node
        else:
            previous.next = next_node

        current.next = None
        self.tail.next = current
        self.tail = current

        return True, "Task moved to the end."

    def traverse_tasks(self, action):
        current = self.head

        while current is not None:
            action(current.task)
            current = current.next

    def count_all_tasks(self):
        total = 0
        current = self.head

        while current is not None:
            total += 1
            current = current.next

        return total

    def count_tasks_by_status(self, status):
        total = 0
        current = self.head

        while current is not None:
            if current.task.status == status:
                total += 1
            current = current.next

        return total