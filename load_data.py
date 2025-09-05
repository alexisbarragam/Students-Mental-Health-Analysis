# load_data.py
from sqlalchemy import create_engine
# Importa a função de limpeza do outro arquivo
from explore_data import clean_student_data, FILE_PATH

# --- Suas informações de conexão ---
DB_USER = 'postgres'
DB_PASSWORD = '05032016'
DB_HOST = 'localhost'
DB_PORT = '1612'
DB_NAME = 'students_mental_health'
# ---------------------------------

CONNECTION_STRING = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def load_clean_data_to_postgres():
    """
    Roda a limpeza dos dados e carrega o DataFrame limpo para o PostgreSQL.
    """
    print("Running data cleaning and preparation script...")
    clean_df = clean_student_data(FILE_PATH)

    if clean_df is not None:
        try:
            engine = create_engine(CONNECTION_STRING)
            print("\nConnecting to PostgreSQL to load data...")

            # Carrega o DataFrame JÁ LIMPO para a tabela 'students'
            clean_df.to_sql('students', engine, if_exists='replace', index=False)
            
            print("\nSUCCESS: Clean data was loaded into your database!")

        except Exception as e:
            print(f"\nERROR: An issue occurred during database loading.")
            print(e)
    else:
        print("\nData loading skipped because the cleaning process failed.")

if __name__ == "__main__":
    load_clean_data_to_postgres()