import streamlit as st
import requests 
import pandas as pd 

API_URL = "http://127.0.0.1:8000"

st.title("Realtime Trend Prediction Dashboard")

st.write("This dashboard is taken data from FastAPI")

# ---Top Words---
st.header("Today vs Yesterday Top Words")
response = requests.get(f"{API_URL}/top-words")
if response.status_code == 200:
    data = response.json()
    today_words = data["today"]["top_words"]
    yesterday_words = data["yesterday"]["top_words"]
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Today - {data["today"]["date"]}")
        st.dataframe(pd.DataFrame(today_words))
    with col2:
        st.subheader(f"Yesterday - {data["yesterday"]["date"]}")
        st.dataframe(pd.DataFrame(yesterday_words))
else:
    st.error("The data is not taken from API")

# ---Trends---
st.header("Top Trend Scores")
trend_response = requests.get(f"{API_URL}/trends")
if trend_response.status_code == 200:
    trends = trend_response.json()
    df_trends = pd.DataFrame(trends)
    st.dataframe(df_trends)
    if not df_trends.empty and "trend_score" in df_trends.columns:
        st.bar_chart(df_trends.set_index("word")["trend_score"])
else:
    st.error("Trend data is not taken.")
