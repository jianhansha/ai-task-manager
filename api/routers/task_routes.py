from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, database
from ..auth import get_current_user
from ..models import User 

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_task(db=db, task=task, user_id=current_user.id)


# ✅ Authenticated route to get all tasks for this user
@router.get("/", response_model=list[schemas.TaskOut])
def get_tasks(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_all_tasks_for_user(db=db, user_id=current_user.id)