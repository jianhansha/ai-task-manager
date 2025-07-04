from crewai import Agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent(Agent):
    def __init__(self, role, goal, backstory, llm=None):

        if llm is None:
            llm = ChatOpenAI(
                temperature=0,
                model=os.getenv("OPENAI_MODEL") or "gpt-3.5-turbo"
            )

        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=llm
        )

    def load_prompt(self, name: str) -> str:
        with open(f"prompts/{name}.txt", "r") as x:
            return x.read()