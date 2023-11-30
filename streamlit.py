import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_use_df(df):
    daily_use_df = df.resample(rule='D', on='order_date').agg({
        "intant": "nunique",
        "casual": "sum",
        "registered" : "sum",
        "cnt" : "sum"
    })
    daily_use_df = daily_use_df.reset_index()
    
    return daily_use_df

def create_season_rent(df):
    season_rent = df.groupby(by="season").agg({
                "casual": "sum",
                "registered": "sum",
                "cnt": "sum"
                })
    return season_rent

def create_weekday_rent(df):
    df['weekday'] = pd.Categorical(df['weekday'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)

    weekday_rent = df.groupby(by="weekday").agg({
                        "casual": "sum",
                        "registered": "sum",
                        "cnt": "sum"
                    })
    return weekday_rent

def create_hour_rent(df):
    hour_rent = df.groupby(by="hr").agg({
                "casual": "sum",
                "registered": "sum",
                "cnt": "sum"
            })
    return hour_rent

def create_timespan_rent(df):
    df["timespan"] = df['hr'].apply(lambda x: 'office hour' if 9 <= x <= 17 else 'non-office hour')

    timespan_rent = df.groupby(by="timespan").agg({
                    "casual": "sum",
                    "registered": "sum",
                    "cnt": "sum"
                })
    return timespan_rent

def create_mnth_rent(df):
    mnth_rent = df.groupby(by="mnth").agg({
                    "casual": "sum",
                    "registered": "sum",
                    "cnt": "sum"
                })
    return mnth_rent

all_df = pd.read_csv("hour_clean.csv")

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()
 
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_date"] >= str(start_date)) & 
                (all_df["order_date"] <= str(end_date))]

daily_use = create_daily_use_df(main_df)
season_rent = create_season_rent(main_df)
weekday_rent = create_weekday_rent(main_df)
hour_rent = create_hour_rent(main_df)
timespan_rent = create_timespan_rent(main_df)
mnth_rent = create_mnth_rent(main_df)

st.header('Simple Dashboard :sparkles:')

st.subheader('Daily Rent')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_use = daily_use.cnt.sum()
    st.metric("Total Bike Rented", value=total_use)
 
with col2:
    total_casual = daily_use.casual.sum() 
    st.metric("Total Casual User", value=total_casual)
 
with col3:
    total_registered = daily_use.registered.sum() 
    st.metric("Total Registered User", value=total_registered)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_use["dteday"],
    daily_use["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
