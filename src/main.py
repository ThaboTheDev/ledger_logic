from ingesters.hist_parser import HistParser
from database.manager import DatabaseManager

inst = HistParser()
with DatabaseManager("data/ledgers.db") as db:
    data = inst.parse("/home/zani/dev/ledger_logic/data/statement-10-20-933-682-8.csv")
    db.apply_categorization()
    
    total_data = db.get_total_summary()
    total_month = db.get_month_summary("2026-02")
    total_data.append(("Net", sum(x for y, x in total_data)))
    total_month.append(("Net", sum(x for y, x in total_month)))
    
    print("--- TOTAL BALANCE BY CATEGORY ---")
    for category, amount_in_cents in total_data:
        print(f"{category}: R{(amount_in_cents) / 100:.2f}")
    
    print("--- FEBRUARY 2026 SPENDING ---")
    for category, amount_in_cents in total_month:
        print(f"{category}: R{(amount_in_cents) / 100:.2f}")