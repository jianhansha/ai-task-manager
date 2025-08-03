from langchain.tools import tool
import dateparser
from .schemas import TaskOut, TaskFilter
from .task_manager import TaskManager


@tool
def get_tasks_with_filters(filter: TaskFilter) -> list[TaskOut]:
    """Fetches and filters tasks from the database based on the given TaskFilter criteria."""
    print(type(filter))
    manager = TaskManager()
    tasks = manager.get_all_tasks()
    filtered = []

    for t in tasks:
        if (
            filter.task_description
            and filter.task_description.lower()
            not in (t.task_description or "").lower()
        ):
            continue
        if (
            filter.task_category
            and filter.task_category.lower() != (t.task_category or "").lower()
        ):
            continue
        if filter.due_date:
            parsed = dateparser.parse(filter.due_date)
            if parsed and t.due_date and t.due_date.date() != parsed.date():
                continue
        if (
            filter.due_date_before
            and t.due_date
            and t.due_date > filter.due_date_before
        ):
            continue
        if filter.due_date_after and t.due_date and t.due_date < filter.due_date_after:
            continue
        if filter.priority and (t.priority or "").lower() != filter.priority.lower():
            continue
        if filter.tags:
            task_tags = [tag.strip().lower() for tag in (t.tags or "").split(",")]
            if not any(tag in task_tags for tag in [tg.lower() for tg in filter.tags]):
                continue
        if filter.is_recurring is not None and t.is_recurring != filter.is_recurring:
            continue
        filtered.append(t)

    return filtered
