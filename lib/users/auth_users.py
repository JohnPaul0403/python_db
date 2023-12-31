#imports
import re

#Auth login
def verify_login(data: dict) -> bool:
    """
    Verifies the login using the provided data.
    Args:
        data (any): The data used for login verification.
    Returns:
        bool: True if the login is verified, False otherwise.
    """
    # Add your login verification logic here
    for key, item in data.items():
        if not item:
            return False
        if type(item) == bool:
            continue
        if any(char == "{" or char == "}" for char in item):
            return False
        if key == "name" and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", item):
            return False
    return True

def verify_google_login(data: dict) -> bool:
    """
    Verifies the Google login using the provided data.
    Args:
        data (dict): The data used for Google login verification.
    Returns:
        bool: True if the Google login is verified, False otherwise.
    """
    # Add your Google login verification logic here
    for key, item in data.items():
        if not item:
            return False
        if type(item) == bool:
            continue
        if key == "name" and not re.match(r"^[a-zA-Z0-9]", item):
            return False
        if key == "email" and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", item):
            return False
    return True 

#Auth signup
def verify_signup(data: dict) -> bool:
    """
    Verify the signup data.
    Args:
        data (dict): The signup data to be verified.
    Returns:
        bool: True if the signup data is valid, False otherwise.
    """
    for key, item in data.items():
        if not item:
            return False
        #Seach for special characters, that could potentially generate vuneverilities to the code
        if any(char == "{" or char == "}" for char in item):
            return False
        if key == "email" and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", item):
            return False
        if key == "pass" and not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$", item):
            return False
    return True

def verify_update(data: dict):
    """
    Verify the update data.
    Args:
        data (dict): The update data to be verified.
    Returns:
        bool: True if the update data is valid, False otherwise.
    """
    for key, item in data.items():
        if not item:
            return False
        if any(char == "{" or char == "}" for char in item):
            return False
        if key == "name" and not re.match(r"^[a-zA-Z]", item):
            return False
        if key == "email" and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", item):
            return False
    return True

def verify_password(data: dict):
    """
    Verify the password data.
    Args:
        data (dict): The password data to be verified.
    Returns:
        bool: True if the password data is valid, False otherwise.
    """
    for key, item in data.items():
        if not item:
            return False
        if any(char == "{" or char == "}" for char in item):
            return False
        if key == "pass" and not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", item):
            return False
    return True

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def verify_file(file_name):
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
