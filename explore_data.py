# explore_data.py
import pandas as pd

FILE_PATH = "students_mental_health.csv"

def clean_student_data(path):
    """
    Loads, cleans, transforms, and returns a summary of the student data.
    """
    try:
        df = pd.read_csv(path)

        
        # Capitalizes the first letter of the 'study_year' column (e.g., 'year 1' -> 'Year 1')
        df['Your current year of Study'] = df['Your current year of Study'].str.capitalize()
        # --------------------------------------------------

        new_column_names = {
            'Choose your gender': 'gender',
            'Age': 'age',
            'What is your course?': 'course',
            'Your current year of Study': 'study_year',
            'Do you have Depression?': 'has_depression',
            'Do you have Anxiety?': 'has_anxiety',
            'Do you have Panic attack?': 'has_panic_attack',
            'Did you seek any specialist for a treatment?': 'sought_treatment'
        }

        df.rename(columns=new_column_names, inplace=True)
        
        
        columns_to_keep = list(new_column_names.values())
        df_cleaned = df[columns_to_keep].copy()
        df_cleaned['country'] = 'Bangladesh'
        yes_no_columns = ['has_depression', 'has_anxiety', 'has_panic_attack', 'sought_treatment']
        for col in yes_no_columns:
            df_cleaned[col] = df_cleaned[col].map({'Yes': 1, 'No': 0})
        final_columns_order = [
            'country', 'gender', 'age', 'course', 'study_year',
            'has_depression', 'has_anxiety', 'has_panic_attack', 'sought_treatment'
        ]
        df_final = df_cleaned[final_columns_order]
        
        return df_final

    except FileNotFoundError:
        print(f"ERROR: File not found at '{path}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    print("Running data exploration and cleaning process...")
    cleaned_data = clean_student_data(FILE_PATH)
    if cleaned_data is not None:
        print("\n--- First 5 rows of FINAL cleaned data ---")
        print(cleaned_data.head())
        print("\n--- General DataFrame Info ---")
        cleaned_data.info()
