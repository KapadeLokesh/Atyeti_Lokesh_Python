import pandas as pd

def test_no_null_amount(db_conn):
    df = pd.read_sql(
        "SELECT * FROM silver_data WHERE amount IS NULL",
        db_conn
    )
    assert len(df) == 0
