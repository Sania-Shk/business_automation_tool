import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"


def show_processed_data_page():
    st.title("📊 Processed Data")

    # Check if user is authenticated
    if "auth_token" not in st.session_state:
        st.warning("Please login first!")
        return

    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}
    response = requests.get(f"{BACKEND_URL}/get-processed-data", headers=headers)

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):  # If data is tabular, display as a table
            st.dataframe(data)
        else:
            st.json(data)  # Otherwise, show JSON

    else:
        error_message = response.json().get("error", "Failed to fetch processed data!")
        st.error(f"❌ {error_message}")
