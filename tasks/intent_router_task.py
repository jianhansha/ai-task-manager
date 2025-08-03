from crewai import Task
from agents.base_agent import BaseAgent

def build_intent_router_task(user_input: str, router_agent: BaseAgent) -> Task:
    base_prompt = router_agent.load_prompt("intent_router_prompt")
    return Task(
        description=base_prompt.format(user_input=user_input),
        expected_output="`add_task`, `view_tasks`, `complete_task`, `delete_task`, `update_task`, or `other`",
        agent=router_agent
    )