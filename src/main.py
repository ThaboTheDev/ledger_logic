from ingesters.hist_parser import HistParser
from database.manager import DatabaseManager

inst = HistParser()
with DatabaseManager("data/ledgers.db") as db:
    data = inst.parse("/home/thabothedev/dev/ledger_logic/data/statement-10-20-933-682-8.csv")
    db.save_transactions(data)