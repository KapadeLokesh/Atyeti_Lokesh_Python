import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.file_handling.file_reader import LogProcessor
from src.dao.db_connection import LogDatabase

if __name__ == "__main__":
    log_path = r'C:\Users\LokeshKapde\Documents\New folder\Python Tasks Repo\Python Practice\PairPrograming\PythonProject1\resources\log1.log'

    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "loki",
        "database": "practice"
    }

    processor = LogProcessor(log_path)
    summary = processor.process_data()

    db = LogDatabase(db_config)
    db.create_table()
    db.insert_log_summary(summary, log_path)
