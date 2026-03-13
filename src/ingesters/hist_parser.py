from ingesters.base import Base
from decimal import Decimal
from models.transaction import Transaction
from typing import List
from csv import reader
from datetime import datetime

class HistParser(Base):
    def parse(self, file_path: str) -> List[Transaction]:
        with open(file_path, 'r') as f:
            file_data = reader(f)
            for i in file_data:
                if i[0] == "HIST":
                    print(i)
                    
    def format_date(unformatted_date: str) -> datetime.date:
        pass