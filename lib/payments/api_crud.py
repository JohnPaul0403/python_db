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



