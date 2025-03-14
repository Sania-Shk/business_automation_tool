import streamlit as st

from pages import login, signup, upload, history, processed_data, visualization

st.set_page_config(page_title="Business Data Automation", page_icon="📊")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Signup", "Upload File", "Recent Files", "Processed Data", "Visualization"])

# Navigation Handling
if page == "Login":
    login.show_login_page()

elif page == "Signup":
    signup.show_signup_page()

elif page == "Upload File":
    upload.show_upload_page()

elif page == "Recent Files":
    history.show_history_page()

elif page == "Processed Data":
    processed_data.show_processed_data_page()

elif page == "Visualization":
    visualization.show_visualization_page()
