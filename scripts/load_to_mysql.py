import pandas as pd
import mysql.connector
from db_config import DB_CONFIG

df = pd.read_csv(
    "data/cleaned/josaa_cleaned.csv"
)

conn = mysql.connector.connect(**DB_CONFIG)

cursor = conn.cursor()

insert_query = """
INSERT INTO seat_allotment
(
year,
round_no,
institute,
academic_program,
quota,
seat_type,
gender,
opening_rank,
closing_rank
)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

for _, row in df.iterrows():

    values = (
        int(row["year"]),
        int(row["round"]),
        row["institute"],
        row["academic_program_name"],
        row["quota"],
        row["seat_type"],
        row["gender"],
        int(row["opening_rank"]),
        int(row["closing_rank"])
    )

    cursor.execute(insert_query, values)

conn.commit()

print("Loaded Successfully")

cursor.close()
conn.close()