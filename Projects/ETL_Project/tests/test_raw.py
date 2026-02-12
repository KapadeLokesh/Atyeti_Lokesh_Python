import pandas as pd

def test_raw_loaded(db_conn):
    df = pd.read_sql("SELECT * FROM raw_data", db_conn)
    assert len(df) == 100
