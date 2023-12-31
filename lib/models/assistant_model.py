from lib.users import assistants_crud
from lib.chatbot import chatbot

class Assistant(object):
    def __init__(self):
        self.__id: int = None
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
        client = chatbot.get_client()
        assistant = chatbot.create_assistant(client, data)
        # Connect to the database
        # Create the assistant in the database
        data["assistant_id"] = assistant.id
        conn = assistants_crud.connect_to_database()
        cursor = conn.cursor()
        resp = assistants_crud.create_assistant(cursor, data)
        if resp:
            self.name = data["name"]
            self.assistant_id = data["assistant_id"]
            self.gpt_model = data["gpt_model"]

        conn.commit()
        conn.close()

        return resp
    
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
        conn = assistants_crud.connect_to_database()
        cursor = conn.cursor()
        resp = assistants_crud.delete_assistant(cursor, self.assistant_id)
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
    assistant.gpt_model = data['gpt-model']
    assistant.files = list(map(lambda x : from_json_files(x), data['files']))
    return assistant

class File:
    def __init__(self, file_id: str, file_name: str):
        self.__file_id = file_id
        self.__file_name = file_name
        self.__purpose = None

    @property
    def file_id(self) -> str:
        return self.__file_id
    
    @file_id.setter
    def file_id(self, file_id: str) -> None:
        self.__file_id = file_id
    
    @property
    def file_name(self) -> str:
        return self.__file_name
    
    @file_name.setter
    def file_name(self, file_name: str) -> None:
        self.__file_name = file_name
    
    @property
    def purpose(self) -> str:
        return self.__purpose
    
    @purpose.setter
    def purpose(self, purpose: str) -> None:
        self.__purpose = purpose
    
    def __str__(self):
        return f"File(file_id={self.file_id}, file_name={self.file_name}, purpose={self.purpose})"
    
    def __repr__(self):
        return self.__str__()
    
    def save_file(self) -> bool:
        """
        Saves the file to the database.
        Returns:
            bool: True if the file was saved successfully, False otherwise.
        """
        conn = assistants_crud.connect_to_database()
        cursor = conn.cursor()
        resp = assistants_crud.create_file(cursor, self.to_json())
        return resp

    def to_json(self) -> dict:
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
            'purpose': self.purpose
        }
    
def from_json_files(data: dict) -> File:
    return File(**data)