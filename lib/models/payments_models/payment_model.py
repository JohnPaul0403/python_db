from dataclasses import dataclass
from . import payments_crud

@dataclass
class AmountMoney:
    amount: int
    currency: str

    def to_json(self) -> dict:
        return {
            'amount': self.amount,
            'currency': self.currency
        }

@dataclass
class CardDetails:
    status: str
    card: dict
    entry_method: str
    cvv_status: str
    avs_status: str
    statement_description: str
    card_payment_timeline: dict

    def to_json(self) -> dict:
        return {
            'status': self.status,
            'card': self.card,
            'entry_method': self.entry_method,
            'cvv_status': self.cvv_status,
            'avs_status': self.avs_status,
            'statement_description': self.statement_description,
            'card_payment_timeline': self.card_payment_timeline
        }

@dataclass
class ProcessingFee:
    effective_at: str
    type: str
    amount_money: AmountMoney

    def to_json(self) -> dict:
        return {
            'effective_at': self.effective_at,
            'type': self.type,
            'amount_money': self.amount_money
        }

@dataclass
class ApplicationDetails:
    square_product: str
    application_id: str

    def to_json(self) -> dict:
        return {
            'square_product': self.square_product,
            'application_id': self.application_id
        }

@dataclass
class Payment:
    id: str
    created_at: str
    updated_at: str
    amount_money: AmountMoney
    status: str
    delay_duration: str
    source_type: str
    card_details: CardDetails
    location_id: str
    order_id: str
    risk_evaluation: dict
    processing_fee: list[ProcessingFee]
    total_money: AmountMoney
    approved_money: AmountMoney
    receipt_number: str
    receipt_url: str
    delay_action: str
    delayed_until: str
    application_details: ApplicationDetails
    version_token: str

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'amount_money': self.amount_money.to_json(),
            'status': self.status,
            'delay_duration': self.delay_duration,
            'source_type': self.source_type,
            'card_details': self.card_details.to_json(),
            'location_id': self.location_id,
            'order_id': self.order_id,
            'risk_evaluation': self.risk_evaluation,
            'processing_fee': list(map(lambda x : x.to_json(), self.processing_fee)),
            'total_money': self.total_money.to_json(),
            'approved_money': self.approved_money.to_json(),
            'receipt_number': self.receipt_number,
            'receipt_url': self.receipt_url,
            'delay_action': self.delay_action,
            'delayed_until': self.delayed_until,
            'application_details': self.application_details.to_json(),
            'version_token': self.version_token
        }
    
    def save_payment(self, cursor, user_id: str) -> None:
        payments_crud.create_payment(cursor, user_id, self.to_json())

def from_json(data: dict) -> Payment:
    return Payment(**data["payment"])