import os
import time
import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from dotenv import load_dotenv
from interaction_db.data_sources import (
    DRUG_TO_DRUG_POSITIVE,
    DRUG_TO_DRUG_NEGATIVE,
    SINGLE_DRUG_DATA,
)

load_dotenv()

USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PORT = int(os.getenv("MYSQL_PORT", 3306))
DATABASE = os.getenv("MYSQL_DATABASE")


def wait_for_mysql(host, user, password, port, timeout=60):
    print(f"⏳ Waiting for MySQL at {host}:{port}...")
    start_time = time.time()
    while True:
        try:
            conn = mysql.connector.connect(
                host=host, user=user, password=password, port=port
            )
            conn.close()
            print("MySQL is ready!")
            break
        except Error as e:
            if time.time() - start_time > timeout:
                raise TimeoutError("MySQL did not become ready in time.")
            time.sleep(2)


wait_for_mysql(HOST, USER, PASSWORD, PORT)

# Create the database if it doesn't exist
conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
print(f"Database '{DATABASE}' created or already exists.")
cursor.close()
conn.close()

# Data
file_paths = {
    "drug_to_drug_positive_controls": DRUG_TO_DRUG_POSITIVE,
    "drug_to_drug_negative_controls": DRUG_TO_DRUG_NEGATIVE,
    "single_drug_data": SINGLE_DRUG_DATA,
}

# MySQL
engine = create_engine(
    f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# Process data
for table_key, file_path in file_paths.items():
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    if table_key == "single_drug_data":
        # Load positive and negative controls into separate tables
        sheet_map = {
            "Tab1 - Positive": "single_drug_positive_controls",
            "Tab2 - Negative": "single_drug_negative_controls",
        }
        for sheet_name, table_name in sheet_map.items():
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            df = df.where(pd.notnull(df), None)
            df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
            print(f"Uploaded sheet '{sheet_name}' to table '{table_name}'")
    else:
        df = pd.read_excel(file_path, sheet_name=0)
        df = df.where(pd.notnull(df), None)
        df.to_sql(name=table_key, con=engine, if_exists="replace", index=False)
        print(f"Uploaded file '{file_path}' to table '{table_key}'")

print("All Excel data uploaded to MySQL successfully.")
