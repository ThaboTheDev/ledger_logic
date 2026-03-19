from ingesters.base_ingestor import BaseIngester
from decimal import Decimal
from models.transaction import Transaction
from typing import List
from csv import reader
from datetime import datetime

class CapitecParser(BaseIngester):
    def parse(self, file_path: str) -> List[Transaction]:
        transactions: List[Transaction] = []
        transaction_date: datetime.date
        amount: Decimal
        description: str
        type_code: str
        
        with open(file_path, 'r') as f:
            file_data = reader(f)
            next(file_data)
            for i in file_data:
                if not i: continue
                
                transaction_date = datetime.strptime(i[3].split()[0], "%Y-%m-%d").date()
                
                try:
                    amount = (self._parse_amount(i[8])) + (self._parse_amount(i[9])) + (self._parse_amount(i[10]))
                except Exception as e:
                    print(f"Error parsing row: {e}")
                    continue
                
                description = i[4]
                type_code = i[7]
                
                transactions.append(
                    Transaction(
                        transaction_date, 
                        amount, 
                        description, 
                        type_code
                        )
                    )
        return transactions
    
    @staticmethod
    def _parse_amount(amount: str) -> Decimal:
        if amount == "" or amount == None:
            return Decimal("0.00")
        return Decimal(amount)