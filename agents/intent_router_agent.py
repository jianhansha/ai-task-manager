from agents.base_agent import BaseAgent

class IntentRouterAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Intent Router",
            goal="Determine whether the user wants to add, view, or update tasks",
            backstory="An expert at understanding human intent and routing input to the correct system.",
            llm=llm
        )

