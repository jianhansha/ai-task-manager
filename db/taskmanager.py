from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_description = Column(String)
    due_date = Column(DateTime)
    priority = Column(String)
    tags = Column(String)
    is_recurring = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

class TaskManager:
    project_root = os.path.dirname(os.path.abspath(__file__))
    def __init__(self, db_path=f"sqlite:///{os.path.join(project_root, '..', 'data', 'tasks.db')}"):
        print(db_path)
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_task(self, task_data):
        session = self.Session()
        try:
            due_date_str = task_data.get("due_date")
            due_date = (
                datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
                if due_date_str else None
            )
            def parse_bool(val):
                if isinstance(val, bool):
                    return val
                if isinstance(val, str):
                    return val.strip().lower() in ("true", "1", "yes")
                if isinstance(val, int):
                    return val == 1
                return False
            task = Task(
                task_description=task_data.get("task_description"),
                task_category=task_data.get("task_category"),
                due_date=due_date,
                priority=task_data.get("priority"),
                tags=task_data.get("tags"),
                is_recurring=parse_bool(task_data.get("is_recurring", False)),
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