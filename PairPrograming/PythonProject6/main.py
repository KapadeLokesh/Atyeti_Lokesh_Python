from src.file_handling.file_reader import LogProcessor
from src.dao.db_connection import LogDatabase

if __name__ == "__main__":
    log_path = r'C:\Users\LokeshKapde\Documents\New folder\Python Tasks Repo\Python Practice\PairPrograming\PythonProject6\resources\input'

    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "loki",
        "database": "logProcessor"
    }

    processor = LogProcessor(log_path)
    summaries = processor.process_files()

    db = LogDatabase(db_config)
    db.create_table()

    for log_counts, log_file in summaries:
        db.insert_log_summary(log_counts, log_file)


