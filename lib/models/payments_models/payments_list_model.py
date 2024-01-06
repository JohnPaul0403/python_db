from .payment_model import Payment, from_json

def to_json(data: list[Payment]) -> dict:
    return {
        "payments": list(map(lambda x : x.to_json(), data))
    }

def from_json(data: dict) -> list[Payment]:
    return [from_json({"payment" : payment}) for payment in data["payments"]]