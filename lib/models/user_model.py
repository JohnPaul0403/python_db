from . import assistant_model
from lib.users import user_crud, assistants_crud

class User:
    def __init__(self, email:str):
        self.__id = None
        self.__name = None
        self.__email = email
        self.__password = None
        self.__pro_plan = False
        self.__assistants = None

    #Deletes object for logout
    def __del__(self):
        del self

    #Decorator for password
    def set_password(function):
        """
        Decorator function that checks the validity of a password before executing a given function.

        Parameters:
            function (function): The function to be executed if the password is valid.
            self: The instance of the class calling the decorator.
            password (str): The password to be validated.

        Raises:
            ValueError: If the password is less than 8 characters long.
            ValueError: If the password does not contain at least one digit.
            ValueError: If the password does not contain at least one uppercase letter.
            ValueError: If the password does not contain at least one lowercase letter.

        Returns:
            The result of executing the given function if the password is valid.
        """
        def wrapper(self, password):
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
            if not any(char.isdigit() for char in password):
                raise ValueError("Password must contain at least one digit")
            if not any(char.isupper() for char in password):
                raise ValueError("Password must contain at least one uppercase letter")
            if not any(char.islower() for char in password):
                raise ValueError("Password must contain at least one lowercase letter")
            return function(self, password)
        return wrapper
    
    #Decorator for assistants
    def get_assistants(function):
        """
        Decorator function that checks if the list of assistants is not empty before executing a given function.

        Parameters:
            function (function): The function to be executed if the list of assistants is not empty.
            self: The instance of the class calling the decorator.
            assistants (list): The list of assistants.

        Raises:
            ValueError: If the list of assistants is empty.

        Returns:
            The result of executing the given function if the list of assistants is not empty.
        """
        def wrapper(self, assistants):
            conn = assistants_crud.connect_to_database()
            cursor = conn.cursor()
            get_assistants = assistants_crud.read_assistants(cursor, self.id)
            assistants = list(map(lambda x : assistant_model.from_json(x), get_assistants)) if get_assistants else [0]
            if len(assistants) == 0:
                cursor.close()
                raise ValueError("Assistants list cannot be empty")
            if assistants[-1] == 0:
                assistants.pop()
            cursor.close()
            return function(self, assistants)
        return wrapper
    
    #Attributes setter and getters
    
    #Attributes setter and getters with python decorators
    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> str:
        self.__name = name

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = email

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    @set_password
    def password(self, password: str):
        self.__password = password

    @property
    def pro_plan(self) -> bool:
        return self.__pro_plan

    @pro_plan.setter
    def pro_plan(self, pro_plan: bool):
        self.__pro_plan = pro_plan

    @property
    def assistants(self) -> list:
        return self.__assistants
    
    @assistants.setter
    @get_assistants
    def assistants(self, assistants: list[assistant_model.Assistant]):
        self.__assistants = assistants

    def change_pro_plan(self):
        """
        Changes the pro plan of the user.
        """
        self.pro_plan = not self.pro_plan

    def to_json(self) -> dict:
        """
        Converts the object to a JSON representation.

        Returns:
            dict: A dictionary representing the object in JSON format.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'pro_plan': self.pro_plan,
            'assistants': list(map(lambda x : x.to_json(), self.assistants)) if self.assistants else []
        }
    
    def to_json_for_update(self) -> dict:
        """
        Converts the object to a JSON representation.

        Returns:
            dict: A dictionary representing the object in JSON format.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'pro_plan': self.pro_plan,
        }

    def login(self, password) -> bool:
        """
        Logs in the user with the given password.
        Parameters:
            password (str): The password of the user.
        Returns:
            bool: True if the login is successful, False otherwise.
        """
        conn = user_crud.connect_to_database()
        cursor = conn.cursor()
        user = user_crud.read_user(cursor, self.email)
        if user is None:
            return False
        
        if user[2] != self.email or user[3] != password:
            return False
        
        self.id = user[0]
        self.name = user[1]
        self.email = user[2]
        
        return True

    def login_google(self, user_name) -> bool:
        """
        Logs in a user using their Google credentials.
        Args:
            user_name (str): The username of the user.
        Returns:
            bool: True if the user is successfully logged in, False otherwise.
        """
        conn = user_crud.connect_to_database()
        cursor = conn.cursor()
        user = user_crud.read_user(cursor, self.email)
        if user is None:
            return False
        
        if user[2] != self.email or user[1] != user_name:
            return False
        
        self.id = user[0]
        self.name = user[1]
        self.email = user[2]
        
        return True

    def logout(self, session) -> None:
        """
        Logout the user and remove the user session.

        Args:
            session (unknown_type): The user session.

        Returns:
            None: This function does not return anything.
        """
        session.pop("user", None)

    def signup(self, data: dict) -> bool:
        """
        Creates a new user in the database.
        Args:
            data (dict): A dictionary containing user data.
        Returns:
            bool: True if the user is successfully created, False otherwise.
        """
        conn = user_crud.connect_to_database()
        cursor = conn.cursor()
        self.name = data["username"]
        self.password = data["password"]
        user = user_crud.create_user(cursor, data)
        conn.commit()
        conn.close()
        return user
    
    def update_user(self, data: dict) -> bool:
        """
        Updates a user in the database.
        Args:
            data (dict): A dictionary containing the updated user data.
        Returns:
            bool: True if the user was successfully updated, False otherwise.
        """
        conn = user_crud.connect_to_database()
        cursor = conn.cursor()
        self.name = data["name"]
        self.email = data["email"]
        user = user_crud.update_user(cursor, self.to_json_for_update())
        conn.commit()
        conn.close()
        return user
    
    def update_pro_plan(self, pro_plan: bool) -> bool:
        """
        Updates the pro plan of a user in the database.
        Args:
            pro_plan (bool): The new pro plan status.
        Returns:
            bool: True if the pro plan was successfully updated, False otherwise.
        """
        conn = user_crud.connect_to_database()
        cursor = conn.cursor()
        self.pro_plan = pro_plan
        user = user_crud.update_user(cursor, self.to_json_for_update())
        conn.commit()
        conn.close()
        return user
    
    def update_password(self, password: str) -> bool:
        """
        Updates the password of a user in the database.
        Args:
            password (str): The new password.
        Returns:
            bool: True if the password was successfully updated, False otherwise.
        """
        conn = user_crud.connect_to_database()
        cursor = conn.cursor()
        user_verify = user_crud.read_user_by_id(cursor, self.id)
        print(self.id, user_verify)
        if user_verify is None:
            return False
        print(user_verify[3])
        if user_verify[3] != password["old_password"]:
            return False
        self.password = password["new_password"]
        user = user_crud.update_user_pass(cursor, self.to_json_for_update())
        conn.commit()
        conn.close()
        return user
    
    def delete_user(self) -> bool:
        """
        Deletes a user from the database.
        :return: True if the user was successfully deleted, False otherwise.
        :rtype: bool
        """
        conn = user_crud.connect_to_database()
        cursor = conn.cursor()
        user = user_crud.delete_user(cursor, self.id)
        conn.commit()
        conn.close()
        return user

def from_json(data: dict):
    """
    Creates a User object from a JSON dictionary.
    Args:
        data (dict): A dictionary containing user data.
    Returns:
        User: A User object.
    """
    user = User(data["email"])
    user.name = data["name"]
    user.pro_plan = data["pro_plan"]
    user.id = data["id"]
    user.assistants = list(map(lambda x : assistant_model.from_json(x), data["assistants"]))
    return user