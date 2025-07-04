from crewai import Task
from agents.base_agent import BaseAgent
from datetime import datetime



def build_task_parse_task(user_input: str, agent: BaseAgent) -> Task:
    base_prompt = agent.load_prompt("task_parser_prompt")
    today = datetime.now()
    return Task(
        description=base_prompt.format(user_input=user_input,today=today),
        expected_output="A JSON object with the correct fields and valid data types.",
        agent=agent
    )