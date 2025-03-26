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

            # ✅ Store user session properly
            st.session_state["auth_token"] = data["token"]
            st.session_state["user_id"] = data["user"]["id"]
            st.session_state["user_email"] = data["user"]["email"]  # ✅ Fix: store email too
            st.session_state["user_name"] = data["user"].get("full_name", "User")
            st.session_state["is_logged_in"] = True  # ✅ New session flag

            st.success("✅ Login successful! Redirecting...")
            st.rerun()  # ✅ Force page refresh to apply session

        else:
            st.error(response.json().get("error", "❌ Invalid email or password!"))
