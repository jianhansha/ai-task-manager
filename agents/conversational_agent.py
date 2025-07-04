from agents.base_agent import BaseAgent

class ConversationalAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Conversation Manager",
            goal="Summarize the outcome of tasks and explain to the user what was done in a friendly, natural way",
            backstory="A clear communicator that translates agent results into helpful, human language so users always understand what happened.",
            llm=llm
    )