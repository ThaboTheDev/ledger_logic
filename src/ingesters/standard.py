from ingesters.base_ingestor import BaseIngester
from decimal import Decimal
from models.transaction import Transaction
from typing import List
from csv import reader
from datetime import datetime

class StandardParser(BaseIngester):
    def parse(self, file_path: str) -> List[Transaction]:
        transactions: List[Transaction] = []
        transaction_date: datetime.date
        amount: Decimal
        description: str
        type_code: str
        
        with open(file_path, 'r') as f:
            file_data = reader(f)
            for i in file_data:
                if not i: continue
                
                if i[0] == "HIST":
                    transaction_date = datetime.strptime(i[1].strip(), "%Y%m%d").date()
                    
                    try:
                        amount = Decimal(i[3])
                    except Exception as e:
                        print(F"{e.with_traceback}")
                        continue
                    
                    description = i[4].strip() + " " + i[5].strip() if len(i[5].strip()) > 0 else i[4].strip()
                    type_code = i[6]
                    
                    transactions.append(
                        Transaction(
                            transaction_date, 
                            amount, 
                            description, 
                            type_code
                            )
                        )
        return transactions