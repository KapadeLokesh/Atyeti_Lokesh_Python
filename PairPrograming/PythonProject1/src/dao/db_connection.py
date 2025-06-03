import pymysql

class LogDatabase:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        return pymysql.connect(**self.db_config)

    def create_table(self):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS log_summary (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    info_count INT,
                    warning_count INT,
                    error_count INT,
                    log_file VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("Table `log_summary` created or already exists.")
        finally:
            conn.close()

    def insert_log_summary(self, log_counts, log_file):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO log_summary (info_count, warning_count, error_count, log_file)
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
