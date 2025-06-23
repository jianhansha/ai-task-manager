print("Importing task_bot...")
import agents.task_agent as task_bot

if __name__ == "__main__":
    print("Hi! Welcome to the AI Task Manager")
    agent = task_bot.create_agent()
    task_prompt = input("How can I help you today? ")
    task_prompt += ". Break down this prompt to decipher a JSON with fields relating to a task: Task Description,Due Date, Priority, any relevant tags and is_recurring (true/false)"
    print(task_bot.run_agent(task_prompt,agent))