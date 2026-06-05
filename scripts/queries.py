import mysql.connector
from db_config import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

print("\nTop 10 Most Competitive Programs\n")

query = """
SELECT
    institute,
    academic_program,
    MIN(closing_rank) AS best_closing_rank
FROM seat_allotment
WHERE seat_type='OPEN'
AND gender='Gender-Neutral'
GROUP BY institute, academic_program
ORDER BY best_closing_rank ASC
LIMIT 10;
"""

cursor.execute(query)

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()