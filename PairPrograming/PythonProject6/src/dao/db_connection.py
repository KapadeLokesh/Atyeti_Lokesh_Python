import pymysql
from pycparser.ply.yacc import error_count
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dao.models import Base, LogSummary,ErrorSummary,WarningSummary,InfoSummary

class LogDatabase:
    def __init__(self,db_config):
        self.db_url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
        self.engine = create_engine(self.db_url,echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_table(self):
        Base.metadata.create_all(self.engine)
        print("Table `log_summary6` created or already exists.")

    def insert_log_summary(self,log_counts,log_file):
        session = self.Session()
        try:
            summary = LogSummary(
                info_count= log_counts.get('INFO',0),
                warning_count=log_counts.get("WARNING", 0),
                error_count=log_counts.get("ERROR", 0),
                log_file=log_file
            )
            session.add(summary)
            session.commit()
            print("Log summary inserted successfully.")

        except Exception as e:
            session.rollback()
            print("Failed to insert log summary:", e)

        finally:
            session.close()

    def insert_error(self,log_counts, log_file):
        session = self.Session()
        try:
            errorSummary = ErrorSummary(
                error_count = log_counts.get('ERROR',0),
                log_file = log_file
            )
            session.add(errorSummary)
            session.commit()
            print("Error Summary inserted.")
        finally:
            session.close()

    def insert_warning(self,log_counts, log_file):
        session = self.Session()
        try:
            warningSummary = WarningSummary(
                warning_count = log_counts.get('WARNING',0),
                log_file = log_file
            )
            session.add(warningSummary)
            session.commit()
            print("Warning Summary inserted.")
        finally:
            session.close()

    def insert_info(self,log_counts, log_file):
        session = self.Session()
        try:
            infoSummary = InfoSummary(
                info_count = log_counts.get('INFO',0),
                log_file = log_file
            )
            session.add(infoSummary)
            session.commit()
            print("Info Summary inserted.")
        finally:
            session.close()


class LogDatabase1:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        return pymysql.connect(**self.db_config)

    def create_table1(self):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS log_summary5 (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    info_count INT,
                    warning_count INT,
                    error_count INT,
                    log_file VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("Table `log_summary5` created or already exists.")
        finally:
            conn.close()

    def insert_log_summary1(self, log_counts, log_file):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO log_summary5 (info_count, warning_count, error_count, log_file)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                log_counts.get("INFO", 0),
                log_counts.get("WARNING", 0),
                log_counts.get("ERROR", 0),
                log_file
            ))
            conn.commit()
            print("Log summary inserted successfully.")
        finally:
            conn.close()
