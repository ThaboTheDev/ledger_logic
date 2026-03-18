from ingesters.hist_parser import HistParser
from database.manager import DatabaseManager

inst = HistParser()
with DatabaseManager("data/ledgers.db") as db:
    data = inst.parse("/home/zani/dev/ledger_logic/data/statement-10-20-933-682-8.csv")
    db.apply_categorication()
# import yaml
 
# with open('rules.yaml', 'r') as file:
#     rules = yaml.safe_load(file)
#     categories = rules["categories"]
#     for key, value in categories.items():
#         print(f"Key: {key}, Value: {type(value)}")