import pandas as pd

def test_gold_reconciliation(db_conn):
    silver = pd.read_sql(
        "SELECT SUM(amount) total FROM silver_data",
        db_conn
    )["total"][0]

    gold = pd.read_sql(
        "SELECT SUM(total_amount) total FROM gold_dept_spend",
        db_conn
    )["total"][0]

    assert silver == gold
