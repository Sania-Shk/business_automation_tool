import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:5000"


def show_login_page():
    st.title("🔐 Login")

    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("⚠️ Please enter email and password.")
            return

        response = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})

        if response.status_code == 200:
            data = response.json()

            # ✅ Store user details properly
            st.session_state["auth_token"] = data["token"]
            st.session_state["user_id"] = data["user"].get("id")  # ✅ User ID stored from user_detail table
            st.session_state["user_name"] = data["user"].get("firstname", "User")  # ✅ Firstname stored
            st.session_state["login_message"] = "✅ Login successful!"

            st.rerun()  # ✅ Refresh page after login

        else:
            error_message = response.json().get("error", "❌ Invalid email or password!")
            st.error(error_message)
