import streamlit as st
import requests

# ⬇ Load CSS
def load_css():
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:5000"  # Change this if using a deployed backend

def show_history_page():
    """Streamlit page to display user's upload history."""
    st.title("📜 Upload History")

    # ✅ Ensure user is logged in
    auth_token = st.session_state.get("auth_token")
    if not auth_token:
        st.error("⚠️ Please log in first!")
        st.stop()  # ✅ Stops execution if not logged in

    headers = {"Authorization": f"Bearer {auth_token}"}

    # ✅ Fetch Upload History from API
    with st.spinner("📡 Fetching upload history..."):
        try:
            response = requests.get(f"{API_URL}/history", headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                files = response_data.get("uploaded_files", [])

                if files:
                    st.success(f"✅ Found {len(files)} uploaded files.")

                    # ✅ Display Files in a Table Format
                    file_df = [{"Filename": file['filename'], "Upload Time": file['upload_time']} for file in files]
                    st.dataframe(file_df, use_container_width=True)

                else:
                    st.warning("⚠️ No uploaded files found.")

            elif response.status_code == 401:
                st.warning("⚠️ Session expired. Please log in again.")
                st.session_state.clear()  # ✅ Clears session on token expiry
                st.rerun()

            else:
                error_message = response.json().get("error", "Unknown error")
                st.error(f"❌ Failed to fetch upload history: {error_message}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error: {str(e)}")

# ✅ Run function
if __name__ == "__main__":
    show_history_page()
