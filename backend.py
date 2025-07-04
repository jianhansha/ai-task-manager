from crewai import Crew
from agents.task_parse_agent import TaskParserAgent
from tasks.task_parse_task import build_task_parse_task
from agents.intent_router_agent import IntentRouterAgent
from tasks.intent_router_task import build_intent_router_task
from agents.conversational_agent import ConversationalAgent
from tasks.conversational_task import create_response, create_output_title
from agents.task_SQL_agent import TaskViewerAgent
from agents.show_tasks_agent import ShowTasksAgent
from db.taskmanager import TaskManager
import json
from dotenv import load_dotenv

load_dotenv()  

def build_crew_for_intent(intent: str, user_input: str) -> str | None | None:
    TaskMan = TaskManager()
    chat_agent = ConversationalAgent()
    summary = ""
    if intent == "add_task":
        # parse the user text input into a JSON
        parse_agent = TaskParserAgent()
        parse_task = build_task_parse_task(user_input,parse_agent)
        parse_team = Crew(agents=[parse_agent], tasks=[parse_task], verbose=True)
        parse_result = parse_team.kickoff()
        summary += f"  \n Parsed Task: {parse_result}"

        # store the task in the task db
        task_data = json.loads(parse_result.raw)
        add_result = TaskMan.add_task(task_data)
        if add_result:
            summary += f"  \n Task Successful {add_result}"

        # build message to return to user
        chat_task = create_response(intent,summary,chat_agent)
        chat_team = Crew(agents=[chat_agent], tasks=[chat_task], verbose=True)
        chat_result = chat_team.kickoff()
        return chat_result,None,None

    elif intent == "view_tasks":
        if "today" in user_input.lower() or "high priority" in user_input.lower():
            tasks = ShowTasksAgent.handle_request(user_input)
            output_data = tasks
            summary += f"  \n User requested : {user_input}"
            summary += f"  \n DB returned : {output_data}"
            
        else:
            tasks = TaskViewerAgent.view_tasks(user_input)
            output_data = TaskMan.tasks_to_dataframe(tasks)
            summary += f"  \n User requested : {user_input}"
            summary += f"  \n DB returned : {output_data}"

        chat_task = create_response(intent,summary,chat_agent)
        output_task = create_output_title(chat_task)
        chat_team = Crew(agents=[chat_agent], tasks=[chat_task, output_task], verbose=True)
        result = chat_team.kickoff()
        chat_result = result[0]
        output_title = result[1]
        return chat_result,output_title, output_data
    # Add more mappings later (e.g., view_tasks, complete_task, etc.)
    else:
        return None

def process_user_input(user_input: str):
    router = IntentRouterAgent()
    classification_task = build_intent_router_task(user_input,router)
    intent_crew = Crew(agents=[router], tasks=[classification_task])
    intent_result = intent_crew.kickoff()
    
    intent = intent_result.raw.strip("`").lower()

    reply,output_title,output_data = build_crew_for_intent(intent, user_input)
    if output_title:
        return reply,output_title,output_data
    elif reply:
        return reply,None,None
    else:
        return "❌ Sorry, I couldn't understand or handle that request.",None,None
    
