from lib.users import assistants_crud
from lib import chatbot

class Assistant(object):
    def __init__(self):
        self.__id: int = None
        self.__token: str = None
        self.__name: str = None
        self.__assistant_id: str = None
        self.__gpt_model: str = None
        self.__files: list[File] = []

    #property and setters
    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        self.__id = id

    @property
    def token(self) -> str:
        return self.__token
    
    @token.setter
    def token(self, token: str) -> None:
        self.__token = token

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @property
    def assistant_id(self) -> str:
        return self.__assistant_id
    
    @assistant_id.setter
    def assistant_id(self, assistant_id: str) -> None:
        self.__assistant_id = assistant_id

    @property
    def gpt_model(self) -> str:
        return self.__gpt_model
    
    @gpt_model.setter
    def gpt_model(self, gpt_model: str) -> str:
        self.__gpt_model = gpt_model

    @property
    def files(self) -> list:
        return self.__files
    
    @files.setter
    def files(self, files: list) -> None:
        self.__files = files

    def create_assistant(self, data: dict) -> bool:
        """
        Creates a new assistant in the database.
        Parameters:
            data (dict): A dictionary containing the data for the new assistant.
                - "name" (str): The name of the assistant.
                - "assistant_id" (str): The ID of the assistant.
                - "gpt_model" (str): The GPT model of the assistant.
        Returns:
            bool: True if the assistant was created successfully, False otherwise.
        """
        #Create openai assistant
        print(data)
        client = chatbot.get_client(data["token"])
        assistant = chatbot.create_assistant(client, data)
        # Connect to the database
        # Create the assistant in the database
        data["assistant_id"] = assistant.id
        conn = assistants_crud.connect_to_database()
        cursor = conn.cursor()
        resp = assistants_crud.create_assistant(cursor, data)
        if resp:
            self.__token = data["token"]
            self.__name = data["name"]
            self.__assistant_id = data["assistant_id"]
            self.__gpt_model = data["gpt-model"]
            self.__files = [File(file, self.__assistant_id) for file in data["files"]]
            for file in self.__files:
                file.create_file(cursor)

        conn.commit()
        conn.close()

        return resp
    
    def read_assistant_by_id(self, id: str) -> dict:
        """
        Reads an assistant from the database by ID.
        Parameters:
            id (int): The ID of the assistant to read.
        Returns:
            dict: A dictionary containing the assistant data.
        """
        conn = assistants_crud.connect_to_database()
        cursor = conn.cursor()
        assistant = assistants_crud.read_assistant_by_id(cursor, id)
        conn.close()

        return assistant
    
    def update_assistant(self, data: dict) -> bool:
        """
        Updates an assistant in the database.
        Parameters:
            data (dict): A dictionary containing the data for the updated assistant.
                - "name" (str): The name of the assistant.
                - "assistant_id" (str): The ID of the assistant.
                - "gpt_model" (str): The GPT model of the assistant.
        Returns:
            bool: True if the assistant was updated successfully, False otherwise.
        """
        conn = assistants_crud.connect_to_database()
        cursor = conn.cursor()
        resp = assistants_crud.update_assistant(cursor, data)
        if resp:
            self.name = data["name"]
            self.assistant_id = data["assistant_id"]
            self.gpt_model = data["gpt_model"]

        conn.commit()
        conn.close()

        return resp
    
    def delete_assistant(self) -> bool:
        """
        Deletes an assistant from the database.
        Returns:
            bool: True if the assistant was deleted successfully, False otherwise.
        """
        #Delete openai assistant
        client = chatbot.get_client(self.token)
        chatbot.delete_assistant(client, self.__assistant_id)
        # Connect to the database
        # Delete the assistant from the database
        conn = assistants_crud.connect_to_database()
        cursor = conn.cursor()
        for file in self.__files:
            file.delete_file(client, cursor)
        resp = assistants_crud.delete_assistant(cursor, self.__assistant_id)
        conn.commit()
        conn.close()
        return resp
    
    def get_files_from_crud(self):
        conn = assistants_crud.connect_to_database()
        cursor = conn.cursor()
        self.files = assistants_crud.read_files(cursor, self.assistant_id)
        return self.files
    
    def __str__(self):
        return f"Assistant(name={self.name}, assistant_id={self.assistant_id}, gpt_model={self.gpt_model})"
    
    def __repr__(self):
        return self.__str__()

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'assistant_id': self.assistant_id,
            'gpt_model': self.gpt_model,
            'files': list(map(lambda x : x.to_json(), self.files))
        }
    
def from_json(data: dict) -> Assistant:
    assistant = Assistant()
    assistant.id = data['id']
    assistant.name = data['name']
    assistant.assistant_id = data['assistant_id']
    assistant.gpt_model = data['gpt_model']
    assistant.files = list(map(lambda x : from_json_files(x), data['files']))
    return assistant

class File:
    def __init__(self, file_id: str, assistant_id: str):
        self.__id = None
        self.__file_id = file_id
        self.__assistant_id = assistant_id

    #Properties and setters
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def file_id(self):
        return self.__file_id

    @file_id.setter
    def file_id(self, file_id):
        self.__file_id = file_id

    @property
    def assistant_id(self):
        return self.__assistant_id

    @assistant_id.setter
    def assistant_id(self, assistant_id):
        self.__assistant_id = assistant_id

    #Methods
    def create_file(self, cursor):
        assistants_crud.create_file(cursor, self.to_json())

    def delete_file(self, client, cursor):
        chatbot.delete_file(client, self.__file_id)
        assistants_crud.delete_file(cursor, self.__file_id)

    #Methods
    def to_json(self) -> dict:
        return {
            'id': self.id,
            'file_id': self.file_id,
            'assistant_id': self.assistant_id
        }
    
def from_json_files(data: dict) -> File:
    return File(data["file_id"], data["assistant_id"])