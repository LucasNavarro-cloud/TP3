import streamlit as st
import pandas as pd
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data, remove_data
import os
import glob

import logging

logging.basicConfig(level=logging.INFO)

LAG_N_DAYS: int = 7

os.makedirs("data/raw/", exist_ok=True)
os.makedirs("data/interim/", exist_ok=True)

for file_path in glob.glob("data/raw/*json"):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        logging.warning(e)

st.title("Data Visualization App")

@st.cache_data(ttl=15 * 60)
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(fic_export_data, parse_dates=[col_date])
    return data

df = load_data(LAG_N_DAYS)

# Get the original number of rows
original_rows = len(df)

# Remove data
df, removed_rows = remove_data(df, last_n_samples=4*3)

st.subheader("Total Consumption for Last Week")

# Filter the dataframe to keep only the data for the last week
last_week_start = df[col_date].max() - pd.Timedelta(days=6)
last_week_data = df[df[col_date] >= last_week_start]

# Calculate the total consumption for the last week
total_consumption_last_week = last_week_data[col_donnees].sum()

st.write(f"Total consumption for last week: {total_consumption_last_week}")
st.write(f"Number of rows removed: {removed_rows}")
st.write(f"Original number of rows: {original_rows}")
