import openai
from lib.environments import environments as env

openai.api_key = env.api_key

def get_client():
    """
    Initializes and returns an instance of the OpenAI client.
    Returns:
        An instance of the OpenAI client.
    """
    return openai.OpenAI()

def get_thread(client):
    """
    Get the thread using the provided client.
    Args:
        client (Client): The client object used to connect to the API.
    Returns:
        Thread: The newly created thread object.
    """
    return client.beta.threads.create()

def create_assistant(client, data: dict) -> any:
    """
    Creates a new assistant in the database.
    Args:
        data (dict): A dictionary containing assistant data.
    Returns:
        bool: True if the assistant is successfully created, False otherwise.
    """
    assistant = client.beta.assistants.create(
        name = data["model_name"],
        instructions = data["instructions"],
        model = data["gpt_model"],
        tools = [{"type": "retrieval"}],
        file_ids=data["files"]#Here should be listed all your files
    )

    return assistant

def upload_files_to_openai(client, path):
    """
    Uploads a file to OpenAI.
    Args:
        client (Client): The OpenAI client.
        path (str): The path to the file to be uploaded.
    Returns:
        File: The uploaded file object.
    """
    # Upload a file to OpenAI
    with open(path, 'rb') as file:
        uploaded_file = client.files.create(file=file, purpose='assistants')

    return uploaded_file

def upload_new_files(client, data):
    """
    Uploads a new file to OpenAI and adds it to the assistant.
    Args:
        client (Client): The OpenAI client used to interact with the API.
        data (dict): A dictionary containing the file path and assistant ID.
    Returns:
        None
    """
    # Upload a file to OpenAI
    uploaded_file = upload_files_to_openai(data["file_path"])

    # Add the uploaded file to the assistant
    client.beta.assistants.files.create(assistant_id=data["assistant_id"], file_id=uploaded_file.id)

    print(f"File '{data['file_path']}' uploaded and added to the assistant with ID: {data['assistant_id']}")

def delete_file(client, file_id):
    client.files.delete(file_id)

def send_message(client, thread, m_content) -> None:
    """
    Sends a message to the OpenAI API.
    Args:
        client (Client): The OpenAI client used to interact with the API.
        content (str): The content of the message to be sent.
    Returns:
        Message: The response message object.
    """
    # Send a message to the OpenAI API
    return client.beta.threads.messages.create(thread_id=thread.id,role="user",
        content=m_content
    )

def get_message(client, thread, assistant_id: str) -> list:
    """
    Retrieves messages from a thread using the Watson Assistant API.
    Args:
        client (WatsonClient): The Watson Assistant client.
        thread (Thread): The thread to retrieve messages from.
        assistant_id (str): The ID of the assistant to use.
    Returns:
        list: The list of messages retrieved from the thread, excluding the last one.
    """
    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id=assistant_id,instructions="Be specific and enthusiastic")
    print(run.model_dump_json(indent=4))

    # If run is 'completed', get messages and print
    while True:
    # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
        print(run_status.model_dump_json(indent=4))
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            break

    return messages[:-1]

def filter_messages(messages: list) -> list:
    """
    Filter the messages to extract their values.
    
    Parameters:
        messages (list): The list of messages to be filtered.
        
    Returns:
        list: The filtered message values.
    """
    f_messages: list = [message.value for message in messages.data[1].content]
    return f_messages