from etl.gold_transform import run_gold_aggegrate
from etl.raw_load import run_raw_load
from etl.silver_transformation import run_silver_transformation


def main():
    try:
        print("Starting ETL Pipeline...")

        run_raw_load()
        print("RAW layer completed")

        run_silver_transformation()
        print("SILVER layer completed")

        run_gold_aggegrate()
        print("GOLD layer completed")

        print("ETL Pipeline executed successfully")

    except Exception as e:
        print("ETL Pipeline FAILED")
        print(str(e))
        raise

if __name__ == "__main__":
    main()