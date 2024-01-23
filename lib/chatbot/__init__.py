import openai
from lib.extensions import os
from lib.environments import UPLOAD_FOLDER

def check_openai_api_key(api_key) -> bool:
    openai.api_key = api_key
    try:
        openai.models.list()

        openai.api_key = None
        return True
    except openai.AuthenticationError as e:
        print(e)
        return False

def get_client(token:str):
    """
    Initializes and returns an instance of the OpenAI client.
    Returns:
        An instance of the OpenAI client.
    """
    return openai.OpenAI(api_key=token)

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
    print(data)
    files = [upload_files_to_openai(client, f"{UPLOAD_FOLDER}/{file}").id for file in data["files"]]
    assistant = client.beta.assistants.create(
        name = data["name"],
        instructions = data["instructions"],
        model = data["gpt-model"],
        tools = [{"type": "retrieval"}],
        file_ids = files
    )

    data["files"] = files
    print(data)

    return assistant

def get_assistant(client, assistant_id: str):
    """
    Get the assistant using the provided client and assistant_id.
    Args:
        client (Client): The client object used to connect to the API.
        assistant_id (str): The ID of the assistant to retrieve.
    Returns:
        Assistant: The retrieved assistant object.
    """
    return client.beta.assistants.get(assistant_id)

def list_assistants(client, user_id: str):
    """
    Get the list of assistants using the provided client and user_id.
    Args:
        client (Client): The client object used to connect to the API.
        user_id (str): The ID of the user to retrieve assistants for.
    Returns:
        list: A list of assistant objects.
    """
    return client.beta.assistants.list_by_user(user_id)

def delete_assistant(client, assistant_id: str):
    """
    Delete the assistant using the provided client and assistant_id.
    Args:
        client (Client): The client object used to connect to the API.
        assistant_id (str): The ID of the assistant to delete.
    Returns:
        bool: True if the assistant is successfully deleted, False otherwise.
    """
    return client.beta.assistants.delete(assistant_id)

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

    os.remove(path)
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

def delete_file(client, file_id: str):
    """
    Deletes a file using the provided client and file ID.
    Parameters:
        client (Client): The client object used to interact with the file system.
        file_id (str): The ID of the file to be deleted.
    Returns:
        None
    """
    client.files.delete(file_id)

def list_files(client, assistant_id: str):
    """
    Lists files in the OpenAI API.
    Args:
        client (Client): The OpenAI client used to interact with the API.
        assistant_id (str): The ID of the assistant to list files for.
    Returns:
        list: A list of file objects.
    """
    return client.beta.assistants.files.list(assistant_id)

def get_file(client, file_id: str):
    """
    Retrieves a file from the OpenAI API.
    Args:
        client (Client): The OpenAI client used to interact with the API.
        file_id (str): The ID of the file to be retrieved.
    Returns:
        File: The retrieved file object.
    """
    return client.files.retrieve(file_id)

def delete_file_by_assistant(client, assistant_id: str, file_id: str) -> None:
    """
    Deletes a file from the OpenAI API.
    Args:
        client (Client): The OpenAI client used to interact with the API.
        file_id (str): The ID of the file to be deleted.
    Returns:
        None
    """
    client.beta.assistants.files.delete(assistant_id, file_id)

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

    return messages

def filter_messages(messages: list) -> list:
    """
    Filter the messages to extract their values.
    
    Parameters:
        messages (list): The list of messages to be filtered.
        
    Returns:
        list: The filtered message values.
    """
    f_messages: list = [message.text.value for message in messages.data[0].content]
    return f_messages