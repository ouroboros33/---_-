import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="ИАС - Мониторинг", layout="wide")
st.title("Информационно-аналитическая система")

try:
    conn = psycopg2.connect(
        host="timescaledb",
        port=5432,
        dbname="dwh",
        user="dwh_user",
        password="dwh_pass"
    )
    st.success("✅ Подключение к базе данных установлено")
    df = pd.read_sql("SELECT NOW() as current_time", conn)
    st.write(df)
except Exception as e:
    st.error(f"❌ Ошибка подключения: {e}")