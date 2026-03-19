import sqlite3
from decimal import Decimal, ROUND_HALF_UP
import pathlib
from typing import Self, Tuple, List
from models.transaction import Transaction
import yaml
import re

class DatabaseManager:    
    def __init__(self, file_path: str) -> None:
        path_obj = pathlib.Path(file_path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        self.database_path = path_obj
        
    def __enter__(self) -> Self:
        self.connection = sqlite3.connect(self.database_path)
        self.connection.execute('PRAGMA foreign_keys = ON;')
        self.cursor = self.connection.cursor()
        self._create_tables()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.connection.commit()
        self.connection.close()
        
    def _create_tables(self) -> None:
        sql_command: str = """CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            t_date TEXT NOT NULL,
            amount_cents INTEGER NOT NULL,
            description TEXT NOT NULL,
            type_code TEXT,
            category TEXT DEFAULT 'Uncategorized',
            UNIQUE(t_date, amount_cents, description)
        );"""
        self.cursor.execute(sql_command)
        
    def save_transactions(self, transactions: List[Transaction]) -> None:
        sql_command: str = """
        INSERT OR IGNORE INTO transactions (t_date, amount_cents, description, type_code) VALUES (?, ?, ?, ?)
        """
        save_data: List[Tuple[str, int, str, str]] = []
        for transaction in transactions:
            save_data.append(
                (
                    str(transaction.date), 
                    self._to_cents(transaction.amount),
                    transaction.description,
                    transaction.type_code
                )
            )
        self.cursor.executemany(sql_command, save_data)
        
    def apply_categorization(self):
        with open('rules.yaml', 'r') as file:
            rules = yaml.safe_load(file)["categories"]
                
        fetch_result = self.cursor.execute(
            "SELECT id, description FROM transactions WHERE category = 'Uncategorized'"
        ).fetchall()
        
        to_update = []
        
        for data_id, data_description in fetch_result:
            for cat_name, pattern in rules.items():
                if re.search(pattern, data_description, re.IGNORECASE):
                    to_update.append((cat_name, data_id))
                    break
        
        self.cursor.executemany(
            "UPDATE transactions SET category = ? WHERE id = ?", 
            to_update
        )
        
    def get_total_summary(self):
        return self.cursor.execute(
            "SELECT category, SUM(amount_cents) FROM transactions GROUP BY category ORDER BY SUM(amount_cents) ASC"
        ).fetchall()
    
    def get_month_summary(self, month: str):
        return self.cursor.execute(
            "SELECT category, SUM(amount_cents) FROM transactions WHERE t_date LIKE ? GROUP BY category ORDER BY SUM(amount_cents) ASC",
            (month.strip()+"%",)
        ).fetchall()
                
   
    @staticmethod    
    def _to_cents(amount_in_decimal: Decimal) -> int:
        round_value = amount_in_decimal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        cents_in_decimal = round_value * 100
        cents_in_int = int(cents_in_decimal)
        return cents_in_int