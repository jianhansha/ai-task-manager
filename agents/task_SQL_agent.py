from agents.base_agent import BaseAgent
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class TaskViewerAgent(BaseAgent):
    def __init__(self, llm=None):
        project_root = os.path.dirname(os.path.abspath(__file__))
        db_path = f"sqlite:///{os.path.join(project_root, '..', 'data', 'tasks.db')}"
        db = SQLDatabase.from_uri(db_path)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        self.agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

        super().__init__(
            role="Task Viewer",
            goal="Fetch and summarize relevant tasks based on user's request.",
            backstory="A database specialist with full access to the user's task database. Can understand SQL and retrieve or summarize tasks on request.",
            llm=llm
        )

    def view_tasks(self, query: str) -> str:
        return self.agent_executor.run(query)