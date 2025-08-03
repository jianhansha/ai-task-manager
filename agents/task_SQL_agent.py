from agents.base_agent import BaseAgent
from db.task_tools import get_tasks_with_filters
from db.schemas import TaskFilter
import json
import dateparser
from dotenv import load_dotenv

load_dotenv()


class TaskViewerAgent(BaseAgent):

    def __init__(self, llm=None):
        super().__init__(
            role="Task Viewer",
            goal="View, filter, and summarize tasks based on user request.",
            backstory="A helpful assistant with access to the user's task database who can interpret and respond to task-related queries.",
            llm=llm,
        )

        self.tools = [get_tasks_with_filters]

    def parse_filters(self, user_input: str) -> TaskFilter:
        prompt = self.load_prompt("extract_filters_prompt")
        response = self.llm.call(prompt.format(user_input=user_input))
        try:
            filters_raw = json.loads(response)
        except json.JSONDecodeError:
            filters_raw = {}

        def parse_date_safe(date_str):
            try:
                return dateparser.parse(date_str)
            except Exception:
                return None

        tf = TaskFilter()
        tf.task_description = filters_raw.get("task_description")
        tf.task_category = filters_raw.get("task_category")
        tf.due_date = filters_raw.get("due_date")
        tf.priority = filters_raw.get("priority")

        tags = filters_raw.get("tags")
        if isinstance(tags, str):
            tf.tags = [t.strip() for t in tags.split(",")]
        elif isinstance(tags, list):
            tf.tags = [str(t).strip() for t in tags]
        else:
            tf.tags = None

        is_rec = filters_raw.get("is_recurring")
        if isinstance(is_rec, bool):
            tf.is_recurring = is_rec
        elif isinstance(is_rec, str):
            tf.is_recurring = is_rec.lower() in ["true", "1", "yes"]
        else:
            tf.is_recurring = None

        due_before = filters_raw.get("due_date_before")
        due_after = filters_raw.get("due_date_after")
        tf.due_date_before = parse_date_safe(due_before) if due_before else None
        tf.due_date_after = parse_date_safe(due_after) if due_after else None

        return tf

    def view_tasks(self, user_input: str):
        filters = self.parse_filters(user_input)
        tasks = get_tasks_with_filters(filters)
        return tasks
