import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"  # Flask API URL

def show_signup_page():
    st.title("📝 Signup")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if not full_name or not email or not password:
            st.warning("All fields are required!")
            return

        response = requests.post(f"{BACKEND_URL}/signup", json={
            "full_name": full_name,
            "email": email,
            "password": password
        })

        if response.status_code == 201:
            st.success("Signup Successful! Now login.")
        else:
            st.error(response.json().get("error", "Signup failed!"))


