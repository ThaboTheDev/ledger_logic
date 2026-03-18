from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class Transaction:
    date: date
    amount: Decimal
    description: str
    type_code: str
    category: str = "Uncategorized"
    
    def to_string(self) -> None:
        print(f"""
              Date: {self.date}
              Amount: {self.amount}
              Description: {self.description}
              Type Code: {self.type_code}
              Category: {self.category}
              """)    