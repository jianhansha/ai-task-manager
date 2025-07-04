from agents.base_agent import BaseAgent

class TaskParserAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Task Parser",
            goal="Extract structured task info like title, priority, deadline, and category from user input",
            backstory="An NLP expert skilled at understanding natural language and turning it into actionable task data.",
            llm=llm
        )