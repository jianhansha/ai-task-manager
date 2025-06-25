from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

from datetime import date
today_str = date.today().isoformat()

load_dotenv()

project_root = os.path.dirname(os.path.abspath(__file__))
chosen_model = os.getenv("OPENAI_MODEL")

def load_prompt_template(filename: str) -> str:
    file_path = os.path.join(project_root, "..", "prompts", filename)
    with open(file_path, "r") as f:
        return f.read()

llm = ChatOpenAI(temperature=0,model_name=chosen_model
                 )
    
response_schemas = [
    ResponseSchema(name="task_description", description="A short summary of what needs to be done"),
    ResponseSchema(name="task_category", description="The category closests associated to the task,  like 'work', 'personal', 'fitness'"),
    ResponseSchema(name="due_date", description="When it should be completed, as an ISO 8601 string (e.g. 2025-06-30T10:00:00)"),
    ResponseSchema(name="priority", description="High, Medium, or Low"),
    ResponseSchema(name="tags", description="Relevant tags for the task, added information important to know with the task"),
    ResponseSchema(name="is_recurring", description="true or false, whether the task repeats regularly")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

prompt_template = load_prompt_template("task_parser_prompt.txt")

prompt = ChatPromptTemplate.from_template(prompt_template)

def parse_task(user_input: str) -> dict:
    formatted_prompt = prompt.format_prompt(
        today=today_str,
        user_input=user_input,
        format_instructions=format_instructions
    )
    messages = formatted_prompt.to_messages()
    response = llm.invoke(messages)
    parsed = output_parser.parse(response.content)
    return parsed