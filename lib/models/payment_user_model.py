from dataclasses import dataclass

@dataclass
class Payment_user:
    id: str
    name: str
    token: str
    created_at: str
    updated_at: str

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'token': self.token,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
def from_json(data: dict) -> 'Payment_user':
    return Payment_user(
        id = data['id'],
        name = data['name'],
        token = data['token'],
        created_at = data['created_at'],
        updated_at = data['updated_at']
    )