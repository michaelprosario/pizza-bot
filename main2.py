import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get project end point from environment variable
project_endpoint = os.environ["PROJECT_ENDPOINT"]
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint)

agent = project.agents.get_agent("asst_9CnvIDvhPyCaQU3cgIsJy2fN")

thread = project.agents.threads.get("thread_ZthKaydaa4ihxApVT53yyE6N")

def printLatestMessage(messages):
    messageList = list(messages)
    if messageList and len(messageList) > 0:
        latest_message = messageList[0]
        if latest_message.text_messages:
            print(f"{latest_message.role}: {latest_message.text_messages[-1].text.value}")

while True:
    # get string from user using console
    user_input = input(">")

    message = project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id)

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    else:
        messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING)
        printLatestMessage(messages)



