# analyze_data.py
import pandas as pd
from sqlalchemy import create_engine, text


DB_USER = 'postgres'
DB_PASSWORD = '05032016'
DB_HOST = 'localhost'
DB_PORT = '1612'
DB_NAME = 'students_mental_health'
# ------------------------------------


CONNECTION_STRING = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# This query calculates the percentage of students with mental health issues
# grouped by their year of study.
ANALYSIS_QUERY = """
SELECT
    study_year,
    COUNT(*) AS student_count,
    -- The average of a 0/1 column is the proportion of 1s (e.g., the rate of depression)
    ROUND(AVG(has_depression) * 100, 2) AS depression_rate_percent,
    ROUND(AVG(has_anxiety) * 100, 2) AS anxiety_rate_percent,
    ROUND(AVG(has_panic_attack) * 100, 2) AS panic_attack_rate_percent
FROM
    students
GROUP BY
    study_year
ORDER BY
    study_year ASC;
"""

def perform_analysis():
    """
    Connects to the database, runs the new analysis query, and prints the result.
    """
    try:
        engine = create_engine(CONNECTION_STRING)
        
        print("Performing analysis on the database...")
        with engine.connect() as connection:
            result_df = pd.read_sql_query(text(ANALYSIS_QUERY), connection)

        print("\n--- Student Mental Health Analysis by Year of Study ---")
        print(result_df)

    except Exception as e:
        print(f"\nERROR: An issue occurred during the analysis.")
        print(e)

if __name__ == "__main__":
    perform_analysis()
