from ingesters.base_ingestor import BaseIngester
from decimal import Decimal
from models.transaction import Transaction
from typing import List
from csv import reader
from datetime import datetime

class AbsaParser(BaseIngester):
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
                
                transaction_date = datetime.strptime(i[0].strip(), "%Y%m%d").date()
                
                try:
                    amount = Decimal(i[2])
                except Exception as e:
                    print(f"Error parsing row: {e}")
                    continue
                
                description = i[1]
                if amount < 0:
                    type_code = "ABSA_DEBIT"
                else:
                    type_code = "ABSA_CREDIT"
                
                transactions.append(
                    Transaction(
                        transaction_date, 
                        amount, 
                        description, 
                        type_code
                        )
                    )
        return transactions