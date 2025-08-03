from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .schemas import Task, TaskOut
from datetime import datetime
import os
import pandas as pd

Base = declarative_base()


class TaskManager:
    project_root = os.path.dirname(os.path.abspath(__file__))

    def __init__(
        self,
        db_path=f"sqlite:///{os.path.join(project_root, '..', 'data', 'tasks.db')}",
    ):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_task(self, task_data):
        session = self.Session()
        try:
            due_date_str = task_data.get("due_date")
            due_date = (
                datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M:%S")
                if due_date_str
                else None
            )

            def parse_bool(val):
                if isinstance(val, bool):
                    return val
                if isinstance(val, str):
                    return val.strip().lower() in ("true", "1", "yes")
                if isinstance(val, int):
                    return val == 1
                return False

            recurring = parse_bool(task_data.get("is_recurring", False))

            def combine_list(val):
                if isinstance(val, list):
                    return ",".join(val)
                else:
                    return val

            tag_str = combine_list(task_data.get("tags"))
            task = Task(
                task_description=task_data.get("task_description"),
                task_category=task_data.get("task_category"),
                due_date=due_date,
                priority=task_data.get("priority"),
                tags=tag_str,
                is_recurring=recurring,
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        finally:
            session.close()

    def get_all_tasks(self):
        session = self.Session()
        tasks = session.query(Task).order_by(Task.due_date).all()
        session.close()
        return tasks

    def process_task_data(task_data):
        tags_list = [tag.strip() for tag in task_data.get("tags").split(",")]

    @staticmethod
    def tasks_to_dataframe(tasks: list[TaskOut]) -> pd.DataFrame:
        if not tasks:
            return pd.DataFrame()

        task_dicts = []
        for task in tasks:
            task_dicts.append(
                {
                    "ID": task.id,
                    "Description": task.task_description,
                    "Category": task.task_category,
                    "Due Date": (
                        task.due_date.strftime("%Y-%m-%d %H:%M")
                        if task.due_date
                        else None
                    ),
                    "Priority": task.priority,
                    "Tags": task.tags,
                    "Recurring": "Yes" if task.is_recurring else "No",
                }
            )

        return pd.DataFrame(task_dicts)
