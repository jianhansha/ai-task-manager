from sqlalchemy.orm import Session
import json
from . import models, schemas

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    task_data = task.model_dump()
    if 'tags' in task_data and isinstance(task_data['tags'], list):
        task_data['tags'] = json.dumps(task_data['tags'])

    db_task = models.Task(**task_data, user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_all_tasks_for_user(db: Session, user_id: int):
    tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()
    for task in tasks:
        if isinstance(task.tags, str):
            try:
                task.tags = json.loads(task.tags)
            except json.JSONDecodeError:
                task.tags = []
    return tasks
    