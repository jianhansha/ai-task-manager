
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import os

load_dotenv()

project_root = os.path.dirname(os.path.abspath(__file__))
chosen_model = os.getenv("OPENAI_MODEL")

db_path = f"sqlite:///{os.path.join(project_root, '..', 'data', 'tasks.db')}"
db = SQLDatabase.from_uri(db_path)
llm = ChatOpenAI(temperature=0, model=chosen_model)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True
)