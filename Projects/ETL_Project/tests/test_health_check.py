import pandas as pd

def test_pipeline_health(db_conn):
    for table in ["raw_data", "silver_data", "gold_dept_spend"]:
        df = pd.read_sql(f"SELECT * FROM {table}", db_conn)
        assert len(df) > 0

