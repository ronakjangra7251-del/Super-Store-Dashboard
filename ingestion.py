import pandas as pd
from datetime import datetime

def load_data():
    """Load SuperStore data and log ingestion."""
    try:
        df = pd.read_excel("Sample - Superstore.xls",engine = "xlrd")

        with open("logs/logs_ingestion.txt","a")as f:
            f.write(f"{datetime.now()} - Data ingested successfully {len(df)} rows)\n")

        return df

    except Exception as e:
        with open("logs_ingestion.txt","a") as f:
            f.write(f"{datetime.now()} - ERROR: {e}\n")
        raise e    