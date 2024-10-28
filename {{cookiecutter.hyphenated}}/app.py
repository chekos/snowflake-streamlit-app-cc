import streamlit as st

from utils.helpers import get_snowflake_session

st.title("Example streamlit app.")
session = get_snowflake_session()
user = session.get_current_role().replace('"', "").replace("_", " ")
st.write(f"Hello, {user.title()}!")
