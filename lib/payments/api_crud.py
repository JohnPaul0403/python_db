from square.client import Client
import os

def get_client():
    return Client(
        access_token = os.environ.get("square_token"),
        environment = "sandbox"
    )

def get_payment(client, payment_id):
    return client.payments.retrieve_payment(payment_id)

def list_payments(client, location_id):
    return client.payments.list_payments(location_id)

def delete_payment(client, payment_id):
    return client.payments.delete_payment(payment_id)

def update_payment(client, payment):
    return client.payments.update_payment(payment)

def create_payment(client, payment):
    return client.payments.create_payment(body = payment)

def get_list_clients(client):
    """
    Retrieves a list of clients from the specified `client` object.
    Args:
        client (object): The client object used to retrieve the list of clients.
    Returns:
        list: A list of client objects retrieved from the `client` object.
    Raises:
        None
    """
    return client.customers.list_customers(
        sort_field = "DEFAULT",
        sort_order = "DESC"
    )

def create_customer(client, data: dict):
    """
    Creates a customer using the provided client and data.
    Args:
        client: The client object used to interact with the API.
        data (dict): A dictionary containing the customer data.
            The dictionary should have the following keys:
                - "name" (str): The given name of the customer.
                - "surname" (str): The family name of the customer.
                - "email" (str): The email address of the customer.
    Returns:
        The created customer object.
    """
    return client.customers.create_customer(
        body = {
            "given_name": data["name"],
            "family_name": data["surname"],
            "email_address": data["email"],
        }
    )