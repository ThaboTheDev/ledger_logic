from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Transaction:
    date: datetime.date
    amount: Decimal
    description: str
    type_code: str
    category: str = "Uncategorized"