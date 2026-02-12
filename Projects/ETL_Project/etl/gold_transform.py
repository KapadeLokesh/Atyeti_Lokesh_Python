from venv import logger
import pandas as pd
from db.connection import get_connection
from utils.constants import SILVER_TABLE, GOLD_TABLE

def run_gold_aggegrate():
    conn = get_connection()

    df = pd.read_sql(f"select * from {SILVER_TABLE}",conn)
    gold_df = df.groupby("dept",as_index=False).agg(total_amount = ("amount","sum"))

    gold_df.to_sql(GOLD_TABLE,conn, if_exists="replace",index=False)
    conn.close()

    logger.info("Gold layer transformation completed")