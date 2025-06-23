from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import initialize_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from dotenv import load_dotenv
import os

load_dotenv()

def create_agent() -> AgentExecutor:
    llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")
    
    def dummy_func(input_str: str) -> str:
        return "I received: " + input_str

    dummy_tool = Tool(
        name="dummy",
        func=dummy_func,
        description="A dummy tool that simply echoes input."
    )

    tools = [dummy_tool]
    memory = ConversationBufferMemory(memory_key="chat_history")

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, memory=memory, verbose=True
    )
    return agent

def run_agent(prompt: str,agent: AgentExecutor) -> str:
    print("Hi I am your task bot. Messaged Received!")
    print("Processing...")
    return agent.run(prompt)