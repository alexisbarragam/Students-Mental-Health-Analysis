# dashboard.py

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Student Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
)

# --- YOUR CUSTOM COLOR PALETTE ---
CUSTOM_PALETTE = ['#45B649', '#43C6AC', '#DCE35B', '#F8FFAE']
# ---------------------------------

@st.cache_data
def load_data_from_db():
    """
    Connects to the PostgreSQL database and retrieves the necessary data.
    Returns two dataframes: one with the raw data and one with the analysis results.
    """
    # --- Your Credentials ---
    DB_USER = 'postgres'
    DB_PASSWORD = '05032016'
    DB_HOST = 'localhost'
    DB_PORT = '1612'
    DB_NAME = 'students_mental_health'
    # --------------------------
    
    connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(connection_string)

    analysis_query = """
        SELECT
            study_year,
            COUNT(*) AS student_count,
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
    
    raw_data_query = "SELECT * FROM students;"
    
    with engine.connect() as connection:
        analysis_df = pd.read_sql_query(text(analysis_query), connection)
        raw_df = pd.read_sql_query(text(raw_data_query), connection)
        
    return analysis_df, raw_df

# Load the data
analysis_df, raw_df = load_data_from_db()


# --- Start of the Dashboard Interface ---

st.title("🧠 Student Mental Health Analysis")

st.markdown("""
This dashboard presents an exploratory data analysis of student mental health,
based on a public dataset from Kaggle.
""")

st.header("Analysis by Year of Study")
st.dataframe(analysis_df)

st.markdown("---")

st.header("Interactive Visualizations")

# Chart 1: Bar Chart
fig1 = px.bar(
    analysis_df,
    x="study_year",
    y="depression_rate_percent",
    title="Depression Rate (%) by Year of Study",
    labels={'study_year': 'Year of Study', 'depression_rate_percent': 'Depression Rate (%)'},
    color="study_year",
    color_discrete_sequence=CUSTOM_PALETTE 
)
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Chart 2: Pie Chart
    fig2 = px.pie(
        raw_df,
        names="gender",
        title="Gender Distribution in the Sample",
        hole=0.3,
        color_discrete_sequence=CUSTOM_PALETTE
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    # Chart 3: Histogram
    fig3 = px.histogram(
        raw_df,
        x="age",
        title="Age Distribution of Students",
        labels={'age': 'Age'},
        color_discrete_sequence=[CUSTOM_PALETTE[0]] # Using the first color from your palette
    )
    st.plotly_chart(fig3, use_container_width=True)