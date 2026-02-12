import pandas as pd
from db.connection import get_connection
from utils.logger import get_logger
from utils.constants import RAW_TABLE


def run_raw_load():
    logger = get_logger()

    df = pd.read_csv(r"data\data.csv")

    conn  = get_connection()
    df.to_sql(RAW_TABLE, conn, if_exists="replace", index = False)

    logger.info("Raw data loaded successfully....")
    conn.close()
