import os
import csv
import pandas as pd
from datetime import datetime

class CSV:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.join(SCRIPT_DIR, "finance_data.csv")
    COLUMNS = ["date", "amount", "category", "details"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls,date,amount,category,details):
        new_entry = {"date":date,
                     "amount":amount,
                     "category":category,
                     "details":details
                     }
        with open(cls.CSV_FILE,"a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully.")

CSV.initialize_csv()
CSV.add_entry("28-07-2025", 1000, "Income","Salary")