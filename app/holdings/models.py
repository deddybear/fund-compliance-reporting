from dataclasses import dataclass
from decimal import Decimal

@dataclass(slots=True, frozen=True)
class Holding:
    instrument_id: str
    instrument_name: str
    asset_class: str
    issuer_name: str
    issuer_type: str
    parent_issuer: str
    credit_rating: str
    downgraded_from: str
    market_value_sgd: Decimal
    modified_duration: Decimal