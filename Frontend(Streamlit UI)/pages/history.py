import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"  # ✅ Flask Backend URL


def show_history_page():
    st.title("📜 Upload History")
    st.write("View your previously uploaded files.")

    token = st.session_state.get("auth_token")  # ✅ Fetch Auth Token
    if not token:
        st.error("⚠️ Please log in first!")
        return

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{BASE_URL}/history", headers=headers)
        if response.status_code == 200:
            files_data = response.json().get("files", [])

            if not files_data:
                st.info("📂 No files uploaded yet.")
            else:
                st.write("✅ **Your Uploaded Files:**")
                for file in files_data:
                    st.write(f"📁 **{file['filename']}** - ⏰ {file['upload_time']}")

        else:
            st.error(f"❌ Failed to fetch history: {response.json().get('error', 'Unknown error')}")

    except Exception as e:
        st.error(f"❌ Error fetching history: {str(e)}")


# ✅ Call function if script runs
if __name__ == "__main__":
    show_history_page()
