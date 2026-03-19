from simpleTaskList import TaskService
from taskApp import TaskApp


def main():
    service = TaskService()
    app = TaskApp(service)
    app.mainloop()


if __name__ == "__main__":
    main()