from crewai import Task
from agents.base_agent import BaseAgent

def create_response(intent: str, input: str, agent: BaseAgent) -> Task:
    base_prompt = agent.load_prompt("reply_prompt")
    return Task(
        description=base_prompt.format(intent=intent,input=input),
        expected_output="A conversational output to be printed back to the user",
        agent=agent
    )

def create_output_title(task1 : Task, agent: BaseAgent) -> Task:
    return Task(
        description="Generate a short, relevant title for the summary.",
        expected_output="A concise and appropriate title.",
        agent=agent,
        context=[task1]
    )