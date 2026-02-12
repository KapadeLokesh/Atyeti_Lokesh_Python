import pandas as pd
from db.connection import get_connection
from utils.logger import get_logger
from utils.constants import RAW_TABLE, SILVER_TABLE, VALID_STATUS


def run_silver_transformation(): 

    logger = get_logger()
    conn = get_connection()

    df = pd.read_sql(f"select * from  {RAW_TABLE}",conn)

    df_silver = (
        df.drop_duplicates(subset=["txn_id"])
        .dropna(subset = ["amount"])
        .query(f"status == '{VALID_STATUS}'")
    )

    df_silver.to_sql(SILVER_TABLE, conn, if_exists="replace", index = False)

    logger.info("Silver transformation complete.")

    conn.close()

