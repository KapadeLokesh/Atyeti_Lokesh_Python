import pandas as pd

def test_invalid_status_not_in_silver(db_conn):
    df = pd.read_sql(
        "SELECT * FROM silver_data WHERE status != 'COMPLETED'",
        db_conn
    )
    assert len(df) == 0
