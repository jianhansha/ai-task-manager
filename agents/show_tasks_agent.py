from db.task_manager import TaskManager
from datetime import datetime, timedelta


class ShowTasksAgent:
    def __init__(self):
        self.task_manager = TaskManager()

    def handle_request(self, intent: str) -> list:
        if "today" in intent.lower():
            return self._get_today_tasks()
        elif "high priority" in intent.lower():
            return self._get_by_priority("High")
        elif "all" in intent.lower():
            tasks = self.task_manager.get_all_tasks()
            return self.task_manager.tasks_to_dataframe(tasks)
        else:
            tasks = self.task_manager.get_all_tasks()
            return self.task_manager.tasks_to_dataframe(tasks)

    def _get_today_tasks(self):
        all_tasks = self.task_manager.get_all_tasks()
        today = datetime.today().date()
        filtered_tasks = [
            t for t in all_tasks if t.due_date and t.due_date.date() == today
        ]
        return self.task_manager.tasks_to_dataframe(filtered_tasks)

    def _get_by_priority(self, priority_level):
        all_tasks = self.task_manager.get_all_tasks()
        filtered_tasks = [
            t for t in all_tasks if t.priority.lower() == priority_level.lower()
        ]
        return self.task_manager.tasks_to_dataframe(filtered_tasks)
